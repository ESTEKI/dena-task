from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

import os
from dotenv import load_dotenv
# to display the graph in a notebook 
from IPython.display import display, Image


import agent_src.tools as Tools
import agent_src.prompts as PROMPTS
from . import nodes as Nodes 
import agent_src.logger as Logger

class Agent():
    def __init__(self):
        self.logger = Logger.LoggerManager("task_agent")
        checkpointer = InMemorySaver()
        
        graph_builder = StateGraph(Nodes.AppState)
        graph_builder.add_node("orchestrator",Nodes.orchestrator)
        graph_builder.add_node("search_node",Nodes.search_node)
        graph_builder.add_node("chatbot",Nodes.chat)
        #graph_builder.add_node("tools", self.nodes.tool_node)
        graph_builder.add_edge(START, "orchestrator")
        graph_builder.add_conditional_edges(
            "orchestrator",
            Nodes.should_continue,
            {
                "Statistics": END,
                "Analytical": END,
                "Search": "search_node",
                "Operation": END,
                "None": END
            }
        
)
        # graph_builder.add_edge("tools", "chatbot")

        #graph_builder.add_edge("orchestrator",END)

        self.graph = graph_builder.compile(checkpointer = checkpointer)
        self.logger.log(f"Graph compiled successfully.","Agent")


    def plot(self):
        """Generates and displays a diagram of the graph."""
        try:
            png_data = self.graph.get_graph().draw_mermaid_png()
            display(Image(png_data))
        except Exception as e:
            print(f"Error plotting graph: {e}")
            print("Please ensure you have the required dependencies for graph visualization (e.g., mermaid-cli).")

    def tryInvoke(self, user_input, userID="10"):
        """Invokes the graph with user input and returns a structured response."""
        config = {"configurable": {"thread_id": userID}}
        initial_state = {
            "user_message": user_input,
            "messages": [
                HumanMessage(content=user_input)
            ]
        }

        response = self.graph.invoke(initial_state, config)

        # #try:
        # response_data = response.get('response_json', '{}')
        # data = response_data.get('response', {}).get('data', {})


        return response

        # except (json.JSONDecodeError, KeyError) as e:
        #     self.new_logger.log(f"Error parsing response: {e}", "tryInvoke", level="error")
        #     self.new_logger.log(f"Raw response: {response}", "tryInvoke", level="error")
        #     return {"error": "Failed to parse the response from the graph."}

if __name__ == '__main__':
    print("Agent code")    