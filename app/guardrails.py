CONSEQUENTIAL_ACTIONS = {
    "restart_vmc",
    "create_technician_ticket",
    "send_customer_message",
}


def requires_approval(action: str) -> bool:
    return action in CONSEQUENTIAL_ACTIONS


def validate_action(action: str) -> None:
    if not action or len(action) > 100:
        raise ValueError("Invalid action")
