from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.n8n_service import n8n_service, WORKFLOW_STEPS

router = APIRouter(prefix="/api/n8n", tags=["n8n-workflow"])


class WorkflowTrigger(BaseModel):
    phone_number: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class N8NConfig(BaseModel):
    webhook_url: str
    api_key: str
    n8n_url: str


@router.get("/workflow-steps")
async def get_workflow_steps():
    return {"workflow_name": "WhatsApp Conversation Automation", "steps": WORKFLOW_STEPS}


@router.post("/trigger")
async def trigger_workflow(payload: WorkflowTrigger):
    result = await n8n_service.trigger_webhook(payload.model_dump())
    return result


@router.post("/configure")
async def configure_n8n(config: N8NConfig):
    n8n_service.configure(config.webhook_url, config.api_key, config.n8n_url)
    return {"message": "n8n configured successfully"}
