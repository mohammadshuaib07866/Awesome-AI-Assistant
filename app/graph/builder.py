from langgraph.graph import START, END, StateGraph
from app.graph.nodes.chat_node import chat_node
from langgraph.checkpoint.memory import InMemorySaver
from app.graph.state import ChatbotState


graph = StateGraph(ChatbotState)


## Define the nodes of the graph
graph.add_node("chat_node", chat_node)

## Define the edges of the edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


## Define the checkpointer
checkpointer = InMemorySaver()


## Complile the graph
chatbot = graph.compile(checkpointer=checkpointer)
