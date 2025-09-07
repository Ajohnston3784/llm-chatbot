import logging
from fastapi import APIRouter
from ..schemas import ChatRequest, ChatResponse
from ..rag import query_docs

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logging.info(f"Received chat request: {request.query}")
        answer, sources = query_docs(request.query)

        logging.info(f"Chat response generated.")
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        logging.error(f"Error during chat processing: {e}")
        return {"error": str(e)}
