from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

import agent_src.llm_definition as llms 
import agent_src.prompts as Prompts
import agent_src.utils as Utils
import agent_src.basemodels as Basemodels

@tool
def time_window_extractor_tool(time_expression: str) -> dict:
        """ In this node, we first call the LLm to turn the literal description of time to integers
        Then, manually calculate the dates and output the exact time window."""
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(Basemodels.TimeWindowLLMIntOutput)
        try:  
            #search_criteria = state.get("search_criteria", {})
            print(f"Search criteria received :\n{time_expression}")
            #time_window = search_criteria.get("time_window")
            #print(f"Extracted time window from previous node:\n{time_window}")
            formatted_prompt = Prompts.time_window_extractor_tool_prompt.replace("{time_expression}", str(time_expression))
            #print(f"Formatted prompt for time window extractor node:\n{formatted_prompt}")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            print(f"Exception while building messages for time window extractor tool: {e}")
            formatted_prompt = Prompts.time_window_extractor_node_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]
            return "No time extracted. Failed! {'days' : 0,'months' : 0,'years' : 0}"
        
        try:
            response = str_llm.invoke(messages)
            exact_time = Utils.calculate_date_offset(response.dict(exclude_none=False))
            print(f"LLM response for time window extractor tool:\n{response}")
        except Exception as e:
            print(f"Error in API call to LLM service for time window extractor tool. msg: {e}")
            return {"time_window": None}
        return str(exact_time)
        #return {"time_window": exact_time}

# @tool
# def time_tool(user_input_timeframe: str) -> Dict[str, str]:
#     """
#     Returns current day/date/time: {'day': 'Wednesday', 'date': '2025-11-12', 'time': '14:03:21'}
#     """
#     now = datetime.now()
    
#     return {
#         "day": now.strftime("%A"),
#         "date": now.strftime("%Y-%m-%d"),
#         "time": now.strftime("%H:%M:%S"),
#     }

#     #     Output: {
#     # "start_date": "2026-01-01",   
#     #     "end_date": "2026-01-07"
#     # }