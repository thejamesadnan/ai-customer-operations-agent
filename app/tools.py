from app.data import CUSTOMERS, FAILURES, INVENTORY, MACHINES, SOPS, TRANSACTIONS


def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise ValueError(f"Customer {customer_id} not found")
    return customer


def get_machine(machine_id: str) -> dict:
    machine = MACHINES.get(machine_id)
    if not machine:
        raise ValueError(f"Machine {machine_id} not found")
    return machine


def get_failures(machine_id: str) -> list[dict]:
    return [row for row in FAILURES if row["machine_id"] == machine_id]


def get_transactions(machine_id: str) -> list[dict]:
    return [row for row in TRANSACTIONS if row["machine_id"] == machine_id]


def get_inventory(machine_id: str) -> list[dict]:
    return [row for row in INVENTORY if row["machine_id"] == machine_id]


def get_sop(failure_code: str) -> dict:
    return SOPS.get(
        failure_code,
        {"title": "General escalation", "steps": ["Collect logs and escalate to support."]},
    )
