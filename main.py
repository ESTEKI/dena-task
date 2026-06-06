# we place api end points here

from fastapi import FastAPI,HTTPException
import asyncio

from pydantic import BaseModel
from typing import Dict, Any
from langchain_core.messages import AIMessage

from agent_src.agent import Agent

app = FastAPI()
TaskAgent = Agent()

AGENT_TIMEOUT = 10  # seconds

class ChatRequest(BaseModel):
    conversation_id: str = "s102030"
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    agent_response: str
    last_ai_message: str
    retrieved_data: Dict[str, Any]

@app.post("/chat",response_model=ChatResponse)
async def chat(req: ChatRequest):
    # print(req)
    # response = TaskAgent.tryInvoke(req.message,  str(req.conversation_id))
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                TaskAgent.tryInvoke,
                req.message,
                str(req.conversation_id)
            ),
            timeout=AGENT_TIMEOUT
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Agent response timed out"
        )
    last_ai_msg = response["messages"][-1].content
    print(last_ai_msg)

    return ChatResponse(conversation_id=str(req.conversation_id), agent_response=str(response),last_ai_message=last_ai_msg,retrieved_data=response.get("retrieved_data", {}))

# ---- ROOT ----
@app.get("/")
def root():
    return {"status": "ok", "message": "TaskAgent API is running"}


#uvicorn main:app --host 127.0.0.1 --port 8000