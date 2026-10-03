# AI Customer Operations Agent

A portfolio-grade AI agent for investigating customer operational issues end-to-end.

## What it does

Given an issue such as:

> "Machine MCH-102 has repeated vend failures today. What should I do?"

the MVP:

1. Identifies the customer and machine.
2. Inspects recent failures, transactions, and inventory.
3. Retrieves the relevant operational SOP.
4. Produces structured findings and probable causes.
5. Recommends next actions.
6. Requires approval for consequential actions such as restarting a controller.
7. Records an audit trail, latency, and estimated run cost.

The dataset is synthetic and inspired by real customer-operations workflows. No employer or customer data is included.

## Architecture

```
User
  |
  v
FastAPI
  |
  v
Operations Agent
  |---- Customer / Machine tools
  |---- Failure / Transaction tools
  |---- Inventory tool
  |---- SOP retrieval
  |---- In-memory run history
  |
  v
Guardrails
  |
  +---- approval required for consequential actions
  |
  v
Structured response + audit trail
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open the API docs at `http://127.0.0.1:8000/docs`.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST-001","machine_id":"MCH-102","issue":"Repeated vend failures today"}'
```

The response includes findings, probable causes, recommended actions, approval state, tool calls, latency, and estimated cost.

## Zero-cost design

The current MVP intentionally uses deterministic local data and does not require an external model API. This makes the first milestone reproducible at ₹0 infrastructure/API spend.

## Roadmap

- [x] Tool-based investigation
- [x] Synthetic operational dataset
- [x] Memory abstraction
- [x] Guardrails and approval flags
- [x] Audit logging
- [x] API
- [x] Automated tests
- [x] GitHub Actions CI
- [ ] Real MCP server/transport
- [ ] LLM-backed planner
- [ ] Evaluation dataset and scoring
- [ ] Cost and latency dashboard
- [ ] Free public deployment
- [ ] Demo UI
