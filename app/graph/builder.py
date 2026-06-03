from langgraph.graph import START, END, StateGraph
from app.graph.nodes.chat_node import chat_node, tool_node
from langgraph.checkpoint.memory import InMemorySaver
from app.graph.state import ChatbotState
from langgraph.prebuilt import tools_condition

graph = StateGraph(ChatbotState)


## Define the nodes of the graph
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

## Define the edges of the graph
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")


## Define the checkpointer
checkpointer = InMemorySaver()


## Complile the graph
chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = []
    seen_threads = set()

    for checkpoint in checkpointer.list(None):
        config = getattr(checkpoint, "config", {}) or {}
        thread_id = config.get("configurable", {}).get("thread_id")

        if thread_id and thread_id not in seen_threads:
            seen_threads.add(thread_id)
            all_threads.append({"thread_id": thread_id, "title": "New Chat"})

    return all_threads
