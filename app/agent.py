import time
import uuid

from app.guardrails import requires_approval, validate_action
from app.memory import MemoryStore
from app.models import InvestigationResponse, InvestigateRequest, RecommendedAction, ToolCall
from app.tools import (
    get_customer,
    get_failures,
    get_inventory,
    get_machine,
    get_sop,
    get_transactions,
)


class OperationsAgent:
    def __init__(self) -> None:
        self.memory = MemoryStore()

    def investigate(self, request: InvestigateRequest) -> InvestigationResponse:
        started = time.perf_counter()
        run_id = f"run_{uuid.uuid4().hex[:10]}"
        audit: list[ToolCall] = []

        customer = get_customer(request.customer_id)
        audit.append(ToolCall(name="get_customer", input={"customer_id": request.customer_id}, output=customer))

        machine = get_machine(request.machine_id)
        if machine["customer_id"] != request.customer_id:
            raise ValueError("Machine does not belong to customer")
        audit.append(ToolCall(name="get_machine", input={"machine_id": request.machine_id}, output=machine))

        failures = get_failures(request.machine_id)
        transactions = get_transactions(request.machine_id)
        inventory = get_inventory(request.machine_id)

        audit.extend([
            ToolCall(name="get_failures", input={"machine_id": request.machine_id}, output={"items": failures}),
            ToolCall(name="get_transactions", input={"machine_id": request.machine_id}, output={"items": transactions}),
            ToolCall(name="get_inventory", input={"machine_id": request.machine_id}, output={"items": inventory}),
        ])

        failure_codes = {item["code"] for item in failures}
        findings: list[str] = []
        causes: list[str] = []
        actions: list[RecommendedAction] = []

        if "VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC" in failure_codes:
            count = next(
                item["count"] for item in failures
                if item["code"] == "VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC"
            )
            findings.append(f"{count} failures indicate that the kiosk did not receive an item response from the VMC.")
            causes.append("VMC communication or controller responsiveness issue.")
            sop = get_sop("VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC")
            audit.append(ToolCall(
                name="get_sop",
                input={"failure_code": "VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC"},
                output=sop,
            ))
            action = "restart_vmc"
            validate_action(action)
            actions.append(RecommendedAction(
                action=action,
                reason=f"Follow '{sop['title']}' after confirming there is no active vend.",
                requires_approval=requires_approval(action),
            ))

        if "VEND_FAILED_NUDGE_MAXED" in failure_codes:
            findings.append("Nudge-maxed failures are also present; product alignment or motor resistance should be inspected.")
            causes.append("Product alignment, slot mapping, or motor resistance issue.")
            sop = get_sop("VEND_FAILED_NUDGE_MAXED")
            audit.append(ToolCall(
                name="get_sop",
                input={"failure_code": "VEND_FAILED_NUDGE_MAXED"},
                output=sop,
            ))
            action = "run_controlled_test_vend"
            validate_action(action)
            actions.append(RecommendedAction(
                action=action,
                reason=f"Follow '{sop['title']}' after checking the communication issue.",
                requires_approval=False,
            ))

        if machine["status"] == "offline":
            findings.append("Machine heartbeat is currently offline.")
            causes.append("Power or network connectivity interruption.")
            action = "create_technician_ticket"
            validate_action(action)
            actions.append(RecommendedAction(
                action=action,
                reason="Escalate if the offline state persists beyond the operational SLA.",
                requires_approval=True,
            ))

        low_stock = inventory[0]["low_stock_skus"] if inventory else []
        if low_stock:
            findings.append(f"Low-stock SKUs detected: {', '.join(low_stock)}.")
            causes.append("Inventory availability may contribute to some failed vends.")
            actions.append(RecommendedAction(
                action="refill_low_stock_skus",
                reason="Refill listed low-stock SKUs before treating stock-related failures as resolved.",
                requires_approval=False,
            ))

        if not findings:
            findings.append("No high-signal operational pattern was found in the current dataset.")
            causes.append("Insufficient evidence; gather logs and recent incident context.")
            actions.append(RecommendedAction(
                action="collect_more_evidence",
                reason="Additional evidence is needed before taking a consequential action.",
                requires_approval=False,
            ))

        elapsed_ms = max(1, int((time.perf_counter() - started) * 1000))
        result = InvestigationResponse(
            run_id=run_id,
            customer=customer,
            machine=machine,
            findings=findings,
            probable_causes=causes,
            recommended_actions=actions,
            approval_required=any(a.requires_approval for a in actions),
            audit_log=audit,
            latency_ms=elapsed_ms,
            estimated_cost_usd=0.0,
        )
        self.memory.add({
            "run_id": run_id,
            "customer_id": request.customer_id,
            "machine_id": request.machine_id,
            "issue": request.issue,
        })
        return result
