# dena-task project
dena-task is a conversational AI agent built to handle company tasks in a natural language interface.

## 1.Features
- Handles multi-turn conversations
- Reads data base (.csv) file via an API call from  http://127.0.0.1:8008/search end point.
- Reports Statistics data and Searchs for queries from user input message.
- Uses a workflow conversation management technique to evaluate user intent (search or statistics), extract query entities (e.g. full name, department, time window), and then retrieves data and reports back. 
- Stateful Conversations, keeps all the human and responses related to each session in a conversation via agent State. 
- FastAPI-based HTTP endpoints for integration and error handling

## 2. General architecture of the agent is as follows:
![alt text](image_graph.png)

## 3.Project Structure:
```text

dena-task/
├── agent_src/
│   ├── __init__.py
│   ├── agent.py              # Main agent graph compilation and interfaces
│   ├── basemodels.py         # Pydantic models for LLM output structure
│   ├── llm_definition.py     # GroqAI LLM initialization and configurationI used GroqAI playground cloud service, First, its FREE,
│   │                             second, powerfull models available. I used gpt-oss-120B. Very good understanding of the Persian language, │   │                             and Fast. It is a Mixture-of-Expert model.
│   ├── logger.py             # logging the chatbot output.
│   ├── nodes.py              # Agent graph nodes implementation
│   ├── prompts.py            # System and user prompts for LLM
│   ├── tools.py              # Tool definitions for agent (in development), no tool use implemented for Search and Statistics tasks. Will be 
│   │                             added next.
│   └── utils.py              # Helper functions (date parsing, formatting)
├── dataset/
│   └── main.py               # Dataset API and data filtering logic
│   └── data_prep.py          # Dataset merging and tests on data
├── logs/                     # Agent interaction logs
├── main.py                   # FastAPI application and REST endpoints
├── test_agent.ipynb          # Jupyter notebook for testing and experimentation
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys) (excluded from git for security purposes)
├── .gitignore
├── image_graph.png           # Architecture diagram
└── README.md
```

## 4. Dataset Configuration
The agent uses task data from a CSV file. Searching the data file includes the following columns:


status: Task status (open, closed, in_progress, etc.)

priority: Task priority (critical, high, medium, low)

fullname: Name of the person assigned

department: Department name

assignee_id: Unique identifier for assignee

create_year, create_month, create_day: Task creation date components, when given, all values AFTER these parameters are retrieved.


Note: The dataset module is still under development and may require additional configuration.

## 5. Configuration
1. Set up your GroqAI API key
Create a .env file in the project root with your GroqAI credentials:

Create a `.env` file in the project root with your GroqAI credentials:

```env
api-key = "your_groq_api_key_here"
base-url = "https://api.groq.com/openai/v1"
```

To get a free API key:

Visit console.groq.com

Sign up or log in

Navigate to API Keys section

Generate a new API key

Copy and paste it into your .env file


## 6. Usage
6.1. Create a virtual environment using Anaconda (recommended)
Using Conda:
```bash
conda create -n denatask python=3.11
conda activate denatask
```
And
```bash
pip install -r requirements.txt
```

6.2 Run APIs
- Running the Agent API Server 
```bash
# Start the FastAPI server on localhost:8000
uvicorn main:app --host 127.0.0.1 --port 8000
```
The server will be available at http://localhost:8000

- Running the data bese API server (**in another cmd or terminal) 
```bash
# Start the FastAPI server on localhost:8008
uvicorn main:app --host 127.0.0.1 --port 8008
```
The server will be available at http://localhost:8000

## 7. API Endpoints
Health Check
```bash
GET /
```
Response:

```JSON
{
  "status": "ok",
  "message": "TaskAgent API is running"
}
```
Chat with Agent

```bash
POST /chat
```
Request body:

```JSON
{
  "conversation_id": "s102030",
  "message": "تسکهای باز محمد رضایی را نشان بده"
}

```
Response:

```JSON
{
  "conversation_id": "s102030",
  "agent_response": "...",
  "last_ai_message": "تسک های باز محمد رضایی برای شما ارسال شد.",
  "retrieved_data": {
    "tasks": [...],
    "count": 5
  }
}
```
## 8. Example Queries
```JSON
{
  "conversation_id": "s110022030",
  "message": "تسک های مهدی قنبری رو نشون بده"
}
```


```JSON
{
  "conversation_id": "s110022030",
  "message": "تو سه ماه اخیر"
}
```


RESPONSE to last request:
```JSON
{
  "conversation_id": "s110022030",
  "agent_response": "{'messages': [HumanMessage(content='تسک های مهدی قنبری رو نشون بده', additional_kwargs={}, response_metadata={}, id='68a83b60-aa80-40dd-9a1a-c052b1ecbaa3'), AIMessage(content='موارد پیدا شده برای شما ارسال شد.', additional_kwargs={}, response_metadata={}, id='5f8f46cb-b9ce-4e6c-8a32-c47e8a7cd447', tool_calls=[], invalid_tool_calls=[]), HumanMessage(content='تو سه ماه اخیر', additional_kwargs={}, response_metadata={}, id='be95b5d7-ba6c-4d56-9749-cf498f117740'), AIMessage(content='در بازهٔ سه ماه اخیر، تعداد تسک\\u200cهای مربوط به مهدی قنبری **۲** عدد می\\u200cباشد.', additional_kwargs={}, response_metadata={}, id='c9efe190-87b8-4dde-ab48-fd82863ad703', tool_calls=[], invalid_tool_calls=[])], 'user_intent': 'Search', 'search_criteria': {'time_window': {'day': 6, 'month': 3, 'year': 2026}, 'fullname': 'مهدی قنبری'}, 'retrieved_data': {'count': 2, 'data': [{'Unnamed: 0': 70, 'id': 71, 'title': 'تهیه گزارش عملکرد فصل بهار', 'description': 'ارزیابی خروجی تیم ها', 'create_time': '2026-05-12', 'status': 'Done', 'assignee_id': 21, 'priority': 'Low', 'due_time': '2026/05/30', 'fullname': 'مهدی قنبری', 'department': 'مدیریت', 'create_year': 2026, 'create_month': 5, 'create_day': 12}, {'Unnamed: 0': 120, 'id': 121, 'title': 'بررسی عملکرد مدیران پروژه', 'description': 'تحلیل وضعیت پیشرفت پروژه ها', 'create_time': '2026-06-21', 'status': 'Done', 'assignee_id': 21, 'priority': 'Low', 'due_time': '2026/07/02', 'fullname': 'مهدی قنبری', 'department': 'مدیریت', 'create_year': 2026, 'create_month': 6, 'create_day': 21}]}}",
  "last_ai_message": "در بازهٔ سه ماه اخیر، تعداد تسک‌های مربوط به مهدی قنبری **۲** عدد می‌باشد.",
  "retrieved_data": {
    "count": 2,
    "data": [
      {
        "Unnamed: 0": 70,
        "id": 71,
        "title": "تهیه گزارش عملکرد فصل بهار",
        "description": "ارزیابی خروجی تیم ها",
        "create_time": "2026-05-12",
        "status": "Done",
        "assignee_id": 21,
        "priority": "Low",
        "due_time": "2026/05/30",
        "fullname": "مهدی قنبری",
        "department": "مدیریت",
        "create_year": 2026,
        "create_month": 5,
        "create_day": 12
      },
      {
        "Unnamed: 0": 120,
        "id": 121,
        "title": "بررسی عملکرد مدیران پروژه",
        "description": "تحلیل وضعیت پیشرفت پروژه ها",
        "create_time": "2026-06-21",
        "status": "Done",
        "assignee_id": 21,
        "priority": "Low",
        "due_time": "2026/07/02",
        "fullname": "مهدی قنبری",
        "department": "مدیریت",
        "create_year": 2026,
        "create_month": 6,
        "create_day": 21
      }
    ]
  }
}

```

