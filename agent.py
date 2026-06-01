from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
# import robot.nodes as ROBOT_NODES
# import robot.configs as ROBOT_CONFIGS
# import robot.logger as LOGGER
import os
from dotenv import load_dotenv
# to display the graph in a notebook 
from IPython.display import display, Image

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import SecretStr

import agent_src.tools as Tools
import agent_src.prompts as PROMPTS
import agent_src.nodes as NODES
import agent_src.logger as Logger

class Agent():
    def __init__(self):
        logger = Logger.LoggerManager("task_agent")
        checkpointer = InMemorySaver()
        
        graph_builder = StateGraph(NODES.AppState)
        graph_builder.add_node("chatbot",self.nodes.chatbot)
        #graph_builder.add_node("tools", self.nodes.tool_node)
        graph_builder.add_edge(START, "chatbot")
        # graph_builder.add_conditional_edges(
        #     "chatbot",
        #     self.nodes.should_continue,
        #     {"tools": "tools", "end": END}
        # )
        # graph_builder.add_edge("tools", "chatbot")

        #graph_builder.add_edge("chatbot",END)

        self.graph = graph_builder.compile(checkpointer = checkpointer)
        self.new_logger.log(f"Graph compiled successfully.","Agent")


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
            "user_last_message": user_input,
            "ai_last_message": last_ai_msg,
            "messages": [] # Start with an empty message list for each invocation
        }

        response = self.graph.invoke(initial_state, config)

        try:
            response_data = response.get('response_json', '{}')
            data = response_data.get('response', {}).get('data', {})


            return data

        except (json.JSONDecodeError, KeyError) as e:
            self.new_logger.log(f"Error parsing response: {e}", "tryInvoke", level="error")
            self.new_logger.log(f"Raw response: {response}", "tryInvoke", level="error")
            return {"error": "Failed to parse the response from the graph."}

if __name__ == '__main__':
    print("Agent code")    