# dena-task
A conversational agent for company tasks

## General architecture of the agent is as follows:
![alt text](image_graph.png)



## Project Structure:
# agent_src : 
--agent.py : a code to compile the graph and main interfaces (tryInvoke, plot)
--basemodels.py: structure output of LLM in every node. 
--llm_definition.py: API call to LLM
     I used GroqAI playground cloud service, First, its FREE, second, powerfull models available. I used gpt-oss-120B 
     very good understanding of the Persian language. Fast, because it is Mixture-of-Expert model.
--logger.py: logging the chatbot output.
--nodes.py: Complete list of nodes used in this project.
--prompts.py: Prompts used in LLM calls. 
--tools.py: Empty for now. Unfortunately, I couldnt manage to do all the demo requirments and its not complete.
--utils.py: helper functions such as descriptive time formats to exact day, month and year.

# dataset
Files needed for data prep and loading. It is still needs some working. 


## Some Demo outputs from logs file:
2026-06-04 01:40:26,864 [Agent] [INFO] Graph response: {'messages': [HumanMessage(content='تسکهای باز محمد رضایی را نشان بده', additional_kwargs={}, response_metadata={}, id='4abb1b17-8380-43f5-9ac3-2b9447e16b54')], 'user_intent': 'Search', 'search_criteria': {'status': 'Open', 'fullname': 'محمد رضایی'}}


2026-06-04 16:39:54,148 [Agent] [INFO] Graph response: {'messages': [HumanMessage(content='چند تسک حیاتی تو دوماه گذشته داریم؟', additional_kwargs={}, response_metadata={}, id='e187632b-dd4a-4562-9628-b1333108e5aa')], 'user_intent': 'Statistics', 'search_criteria': {'time_window': 'دوماه گذشته', 'priority': 'Critical'}}



2026-06-04 17:47:35,559 [Agent] [INFO] Graph response: {'messages': [HumanMessage(content='چند تسک حیاتی تو دوماه گذشته داریم؟', additional_kwargs={}, response_metadata={}, id='71aede88-01a1-481c-8f75-9b0293ec7d5b')], 'user_intent': 'Statistics', 'search_criteria': {'time_window': 'دوماه گذشته', 'priority': 'High'}, 'time_window': {'days': 0, 'months': 2, 'years': 0}}
2026-06-04 18:04:07,310 [Agent] [INFO] Graph compiled successfully.

## In this example, the actual date is extracted. Month from 6 to 4. 
2026-06-04 18:04:14,178 [Agent] [INFO] Graph response: {'messages': [HumanMessage(content='چند تسک حیاتی تو دوماه گذشته داریم؟', additional_kwargs={}, response_metadata={}, id='9bff2d6e-1e70-4217-b582-78f78cce4c30')], 'user_intent': 'Statistics', 'search_criteria': {'time_window': 'دوماه گذشته', 'priority': 'Critical'}, 'time_window': {'day': 4, 'month': 4, 'year': 2026}} 

