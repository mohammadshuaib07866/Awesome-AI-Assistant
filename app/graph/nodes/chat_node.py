from app.graph.state import ChatbotState
from app.llms.openai_model import ChatOpenAIModel
from app.tools.tools import calculator, search_tool
import langgraph.prebuilt.tool_node as tool_node_module
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime
from langchain_core.tools import tool

# Ensure the ToolNode module can resolve Runtime annotations during schema inference
tool_node_module.Runtime = Runtime

model = ChatOpenAIModel.get_model()

all_tools = [calculator, search_tool]
model_with_tools = model.bind_tools(all_tools)

tool_node = ToolNode(all_tools)


def chat_node(state: ChatbotState):
    """model node that may answer or request a tool call."""

    messages = state["messages"]

    response = model_with_tools.invoke(messages)

    return {"messages": [response]}
