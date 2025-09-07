from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    docs_ingested: int

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]