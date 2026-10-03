from fastapi import FastAPI, HTTPException

from app.agent import OperationsAgent
from app.models import InvestigateRequest, InvestigationResponse

app = FastAPI(
    title="AI Customer Operations Agent",
    version="0.1.0",
    description="Investigates customer operational incidents using tools, memory, and guardrails.",
)

agent = OperationsAgent()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/investigate", response_model=InvestigationResponse)
def investigate(request: InvestigateRequest) -> InvestigationResponse:
    try:
        return agent.investigate(request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
