from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/rag", tags=["rag"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list


class RecommendRequest(BaseModel):
    query: str
    k: int = 5


@router.post("/chat")
async def chat(req: ChatRequest):
    context = await rag_service.retrieve(req.message)
    response = await rag_service.generate_response(req.message, context)
    return ChatResponse(
        response=response,
        sources=[{"title": d["title"], "content": d["content"][:150] + "..."} for d in context],
    )


@router.post("/recommend")
async def recommend(req: RecommendRequest):
    results = await rag_service.recommend(req.query, k=req.k)
    return {"query": req.query, "recommendations": results}
