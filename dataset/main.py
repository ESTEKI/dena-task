from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class ChatRequest(BaseModel):
    conversation_id: str = "s102030"
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    ai_response: str

@app.post("/read_data",response_model=ChatResponse)
def chat(req: ChatRequest):
    ai_response = TaskAgent.tryInvoke(req.message,  str(req.conversation_id))
    return ChatResponse(user_id=str(req.user_id), ai_response=ai_response)

# ---- ROOT ----
@app.get("/")
def root():
    return {"status": "ok", "message": "TaskAgent API is running"}