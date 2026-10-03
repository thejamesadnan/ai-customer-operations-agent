from pydantic import BaseModel, Field


class InvestigateRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    machine_id: str = Field(min_length=1)
    issue: str = Field(min_length=3)


class ToolCall(BaseModel):
    name: str
    input: dict
    output: dict


class RecommendedAction(BaseModel):
    action: str
    reason: str
    requires_approval: bool = True


class InvestigationResponse(BaseModel):
    run_id: str
    customer: dict
    machine: dict
    findings: list[str]
    probable_causes: list[str]
    recommended_actions: list[RecommendedAction]
    approval_required: bool
    audit_log: list[ToolCall]
    latency_ms: int
    estimated_cost_usd: float
