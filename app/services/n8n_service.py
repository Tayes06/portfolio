import httpx
from typing import Optional, Dict, Any
from pydantic import BaseModel


class N8NWorkflowService:
    def __init__(self):
        self.webhook_url: Optional[str] = None
        self.api_key: Optional[str] = None
        self.n8n_url: Optional[str] = None

    def configure(self, webhook_url: str, api_key: str, n8n_url: str):
        self.webhook_url = webhook_url
        self.api_key = api_key
        self.n8n_url = n8n_url

    async def trigger_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.webhook_url:
            return {"status": "demo", "message": "n8n not configured. This is a demo response.", "payload": payload}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                )
                response.raise_for_status()
                return {"status": "success", "data": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def check_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        if not self.n8n_url or not self.api_key:
            return {"status": "demo", "message": "n8n not configured. Demo mode."}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.n8n_url}/rest/workflows/{workflow_id}",
                    headers={"X-N8N-API-KEY": self.api_key},
                )
                response.raise_for_status()
                return {"status": "success", "data": response.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}


n8n_service = N8NWorkflowService()

WORKFLOW_STEPS = [
    {
        "step": 1,
        "name": "WhatsApp Webhook Trigger",
        "icon": "message-circle",
        "description": "n8n webhook receives incoming WhatsApp messages via Twilio or WhatsApp Business API.",
        "color": "green",
    },
    {
        "step": 2,
        "name": "Message Processing",
        "icon": "filter",
        "description": "Extract sender info, message content, and timestamp. Route based on keywords.",
        "color": "blue",
    },
    {
        "step": 3,
        "name": "AI Intent Classification",
        "icon": "brain",
        "description": "Send message to LLM (OpenAI/Ollama) to classify intent: support, sales, general inquiry.",
        "color": "purple",
    },
    {
        "step": 4,
        "name": "Knowledge Base Query",
        "icon": "database",
        "description": "RAG retrieval from vector DB to find relevant information for the response.",
        "color": "yellow",
    },
    {
        "step": 5,
        "name": "Response Generation",
        "icon": "bot",
        "description": "LLM generates personalized response based on intent + retrieved context.",
        "color": "indigo",
    },
    {
        "step": 6,
        "name": "WhatsApp Reply",
        "icon": "reply",
        "description": "Send generated response back to the user via WhatsApp API.",
        "color": "green",
    },
]
