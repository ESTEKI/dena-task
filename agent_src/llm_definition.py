from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv() 
API_KEY = os.getenv("api-key")
BASE_URL = os.getenv("base-url")

llm_openai = ChatOpenAI(
            api_key = API_KEY,
            base_url=BASE_URL,
            model="openai/gpt-oss-120b",
            reasoning={ "effort": "low" },
            temperature=0.1,
            max_completion_tokens=1024
        )