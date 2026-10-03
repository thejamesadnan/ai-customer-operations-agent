CUSTOMERS = {
    "CUST-001": {
        "customer_id": "CUST-001",
        "name": "Acme Micro Markets",
        "segment": "Enterprise",
    },
    "CUST-002": {
        "customer_id": "CUST-002",
        "name": "Northstar Vending",
        "segment": "SMB",
    },
}

MACHINES = {
    "MCH-101": {
        "machine_id": "MCH-101",
        "customer_id": "CUST-001",
        "location": "Gurugram - HQ",
        "status": "online",
        "model": "Nova",
    },
    "MCH-102": {
        "machine_id": "MCH-102",
        "customer_id": "CUST-001",
        "location": "Gurugram - Plant 2",
        "status": "online",
        "model": "Nova",
    },
    "MCH-201": {
        "machine_id": "MCH-201",
        "customer_id": "CUST-002",
        "location": "Noida - Office",
        "status": "offline",
        "model": "Orion",
    },
}

FAILURES = [
    {"machine_id": "MCH-102", "code": "VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC", "count": 17},
    {"machine_id": "MCH-102", "code": "VEND_FAILED_NUDGE_MAXED", "count": 3},
    {"machine_id": "MCH-101", "code": "VEND_FAILED_CANCELLED_OR_TIMEOUT", "count": 2},
    {"machine_id": "MCH-201", "code": "MACHINE_OFFLINE", "count": 1},
]

TRANSACTIONS = [
    {"machine_id": "MCH-102", "success": 81, "failed": 20, "period": "today"},
    {"machine_id": "MCH-101", "success": 118, "failed": 2, "period": "today"},
    {"machine_id": "MCH-201", "success": 0, "failed": 0, "period": "today"},
]

INVENTORY = [
    {"machine_id": "MCH-102", "low_stock_skus": ["SKU-CHIPS-01"]},
    {"machine_id": "MCH-101", "low_stock_skus": []},
    {"machine_id": "MCH-201", "low_stock_skus": ["SKU-COLA-02"]},
]

SOPS = {
    "VEND_FAILED_NO_ITEM_RESPONSE_FROM_VMC": {
        "title": "VMC no-item-response SOP",
        "steps": [
            "Check kiosk-to-VMC communication logs.",
            "Verify VMC is powered and responsive.",
            "Check the controller communication path.",
            "Restart the VMC only after confirming no active vend.",
            "Escalate to a technician when the issue repeats.",
        ],
    },
    "VEND_FAILED_NUDGE_MAXED": {
        "title": "Nudge-maxed SOP",
        "steps": [
            "Inspect product alignment.",
            "Check motor or spiral resistance.",
            "Validate slot planogram and SKU mapping.",
            "Run a controlled test vend.",
        ],
    },
    "MACHINE_OFFLINE": {
        "title": "Machine offline SOP",
        "steps": [
            "Check connectivity and power.",
            "Check kiosk heartbeat.",
            "Validate network equipment.",
            "Escalate if offline persists beyond SLA.",
        ],
    },
}
