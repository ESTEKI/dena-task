# we place api end points here

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from agent_src import Agent

app = FastAPI()
TaskAgent = Agent()

class ChatRequest(BaseModel):
    conversation_id: str = "s102030"
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    ai_response: str

@app.post("/chat",response_model=ChatResponse)
def chat(req: ChatRequest):
    ai_response = TaskAgent.tryInvoke(req.message,  str(req.conversation_id))
    return ChatResponse(user_id=str(req.user_id), ai_response=ai_response)

# ---- ROOT ----
@app.get("/")
def root():
    return {"status": "ok", "message": "TaskAgent API is running"}


#uvicorn main:app --host 0.0.0.0 --port 8000