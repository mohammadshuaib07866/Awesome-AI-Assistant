from app.graph.state import ChatbotState
from app.llms.openai_model import ChatOpenAIModel

model = ChatOpenAIModel.get_model()


def chat_node(state: ChatbotState):

    messages = state["messages"]

    response = model.invoke(messages)

    return {"messages": [response]}
