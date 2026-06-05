from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated, Literal, Union, Optional, Dict, Any
from . import llm_definition as llms
import agent_src.basemodels as basemodels
import agent_src.prompts as Prompts
import agent_src.utils as Utils
# APPSTATE
class AppState(TypedDict):
            user_msg: str
            messages: Annotated[list, add_messages]
            user_intent: Optional[Literal["Statistics", "Analytical", "Search", "Operation","None"]]
            search_criteria: Optional[Dict[str, Any]]
            time_window: Optional[str]
            retrieved_data: Optional[Dict[str, Any]]

MAX_CONVERSATION_TURNS = 3

def orchestrator(state: AppState):
        """
        Classifier node that determines the action based on last 3 messages in the conversation history. 
        It uses a structured output llm call to determine the user intent and route to the correct node in the graph.
        """
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.OrchestratorClassification)
        messages = state.get("messages", [])

        # Only keep the last 6 messages for context to avoid hitting token limits, and format them for the prompt
        try:
            last_msgs_history = []
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    last_msgs_history.append(f"User: {message.content}")
                elif isinstance(message, AIMessage):
                    last_msgs_history.append(f"Assistant: {message.content}")
                if len(last_msgs_history) == MAX_CONVERSATION_TURNS * 2:
                    break
            last_msgs_history.reverse()

            formatted_prompt = Prompts.orchestrator_prompt.replace("{conversation_history}", str(last_msgs_history))

            #print(f"Formatted prompt for orchestrator:\n{formatted_prompt}")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages: {e}")
            formatted_prompt = Prompts.orchestrator_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]

        try:
            response = str_llm.invoke(messages)
            print(f"User intent in orchestrator Node:{response.intent}")
        except Exception as e:
            print(f"Error in API call to LLM service. msg: {e}")
            return {"user_intent": "None"}
        
        return {"user_intent": response.intent}

def search_node(state: AppState):
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.SearchNodeOutput)
        messages = state.get("messages", []) 
        try:            
            last_msgs_history = []
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    last_msgs_history.append(f"User: {message.content}")
                elif isinstance(message, AIMessage):
                    last_msgs_history.append(f"Assistant: {message.content}")
                if len(last_msgs_history) == MAX_CONVERSATION_TURNS * 2:
                    break
            last_msgs_history.reverse()

            formatted_prompt = Prompts.search_node_prompt.replace("{conversation_history}", str(last_msgs_history))

            #print(f"Formatted prompt for search node:\n{formatted_prompt}")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages for search node: {e}")
            formatted_prompt = Prompts.search_node_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]
        try:
            response = str_llm.invoke(messages)
            print(type(response))
            print(response.dict(exclude_none=True))
        except Exception as e:
            print(f"Error in API call to LLM service for search node. msg: {e}")
            return {"search_criteria": {}}
        return {"search_criteria": response.dict(exclude_none=True), "user_intent": "Search"}

def statistics_node(state: AppState):
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.StatisticsNodeOutput)
        messages = state.get("messages", []) 
        try:            
            last_msgs_history = []
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    last_msgs_history.append(f"User: {message.content}")
                elif isinstance(message, AIMessage):
                    last_msgs_history.append(f"Assistant: {message.content}")
                if len(last_msgs_history) == MAX_CONVERSATION_TURNS * 2:
                    break
            last_msgs_history.reverse()

            formatted_prompt = Prompts.statistics_node_prompt.replace("{conversation_history}", str(last_msgs_history))

            # print(f"Formatted prompt for statistics node:\n{formatted_prompt}")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages for statistics node: {e}")
            formatted_prompt = Prompts.statistics_node_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]
        try:
            response = str_llm.invoke(messages)
            print(f"LLM response for statistics node:\n{response}")
        except Exception as e:
            print(f"Error in API call to LLM service for statistics node. msg: {e}")
            return {"search_criteria": {}}
        return {"search_criteria": response.dict(exclude_none=True), "user_intent": "Statistics"}

def time_window_extractor_node(state: AppState):
        """ In this node, we first call the LLm to turn the literal description of time to integers
        Then, manually calculate the dates and output the exact time window."""
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.TimeWindowLLMIntOutput)
        try:  
            search_criteria = state.get("search_criteria", {})
            print(f"Search criteria received in time window extractor node:\n{search_criteria}")
            time_window = search_criteria.get("time_window")
            print(f"Extracted time window from previous node:\n{time_window}")
            formatted_prompt = Prompts.time_window_extractor_node_prompt.replace("{conversation_history}", str(time_window))
            #print(f"Formatted prompt for time window extractor node:\n{formatted_prompt}")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages for time window extractor node: {e}")
            formatted_prompt = Prompts.time_window_extractor_node_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]
        try:
            response = str_llm.invoke(messages)
            exact_time = Utils.calculate_date_offset(response.dict(exclude_none=False))
            search_criteria["time_window"] = exact_time
            print(f"=======Here is the modified Criteria: {search_criteria}")

            print(f"LLM response for time window extractor node:\n{response}")
        except Exception as e:
            print(f"Error in API call to LLM service for time window extractor node. msg: {e}")
            return {"time_window": None}
        
        
        return {"search_criteria": search_criteria}

def retrieve_data(state: AppState):
        """
        This node calls dataset API and saves them in agent State.
        """
        #user_intent = state.get("user_intent", "None")
        search_criteria = state.get("search_criteria",[])
        time_window = state.get("time_window") or None

        try:
            if search_criteria or time_window:
                retrieved_data = Utils.call_database_api(search_criteria)
                #retrieved_data = Utils.call_database_api(search_criteria, time_window)

                print("API result:", retrieved_data)
        except Exception as e:
            print(f"Error calling API: {e}")
            retrieved_data = {"count": 0, "data": []}
        
        return {"retrieved_data": retrieved_data}


def chat(state: AppState):
        """
        general chat node that takes in user input and returns a response from the llm.
        """

        llm = llms.llm_openai
        #response = llms.llm_openai.invoke(messages)
        messages = state.get("messages", []) 
        user_intent = state.get("user_intent",[])
        
        try:            
            # last_msgs_history = []
            # for message in reversed(messages):
            #     if isinstance(message, HumanMessage):
            #         last_msgs_history.append(f"User: {message.content}")
            #     elif isinstance(message, AIMessage):
            #         last_msgs_history.append(f"Assistant: {message.content}")
            #     if len(last_msgs_history) == 2:
            #         break
            # last_msgs_history.reverse()

            #formatted_prompt = Prompts.chat_node_prompt.replace("{conversation_history}", str(messages))

            retrieved_data = state.get("retrieved_data",[])
            num_tasks = 0

            if retrieved_data and isinstance(retrieved_data, dict):
                num_tasks = retrieved_data.get("count", 0)

            if not user_intent or user_intent == "None":
                user_intent = "Did not understand user intent"
            elif user_intent == "Statistics":
                user_intent = f"User is asking for statistics about the ticketing system data. And the total found number is {num_tasks}"
            elif user_intent == "Search":
                user_intent = f"User is asking for Search about the ticketing system data. And the total found number is {num_tasks}"
            print(f"{user_intent}")
            formatted_prompt = Prompts.chat_node_prompt.replace("{user_intent}", str(user_intent))
            print(formatted_prompt)
            messages = [
                SystemMessage(content=formatted_prompt),
                *messages,
            ]
            
            print(f"Formatted prompt for CHAT node:\n{str(messages)}")
            # messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages for CHAT node: {e}")
            # formatted_prompt = Prompts.statistics_node_prompt.replace("{user_intent}", "failed to load data!")
            # messages = [HumanMessage(content=formatted_prompt)]


        try:
            response = llm.invoke(messages)
            print(f"LLM response for chat node:\n{response}")
        except Exception as e:
            print(f"Error in API call to LLM service for chat node. msg: {e}")
            return {"messages": ["error in call to LLM"]}
        

        # Normalize response.content to a simple string
        if isinstance(response.content, list):
            extracted = []
            for item in response.content:
                if isinstance(item, dict) and "text" in item:
                    extracted.append(item["text"])
            content_text = " ".join(extracted)
        else:
            content_text = str(response.content).strip()
        
        print(f"Chat response: {content_text}")

        
        return {"messages": [AIMessage(content_text)] }

## ---------- Conditional edge functions -----------

def should_continue(state: AppState):
    """
    Routes the flow based on user_intent produced by the orchestrator node.
    """

    user_intent = state.get("user_intent")

    if not user_intent or user_intent == "None":
        return "None"

    intent_map = {
        "Statistics": "Statistics",
        "Analytical": "Analytical",
        "Search": "Search",
        "Operation": "Operation",
    }
    # returning the corresponding node based on user intent, if intent is not recognized return "end"
    return intent_map.get(user_intent, "None")
        
        
def is_time_window_extraction_needed(state: AppState):
    """
    Checks if the user input requires time window extraction based on the presence of a time window in the search criteria.
    If the user intent is "Statistics" and there is a time window mentioned in the search criteria, it returns True, otherwise False.
    """
    user_intent = state.get("user_intent")
    search_criteria = state.get("search_criteria", {})
    
    if user_intent == "Statistics" and search_criteria.get("time_window"):
        print("---------Time window extraction needed based on user intent and search criteria.")
        return "time_window_extractor_node"
    return "end"

