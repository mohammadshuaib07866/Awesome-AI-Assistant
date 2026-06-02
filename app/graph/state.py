from typing import Annotated, TypedDict
from langgraph.graph import add_messages


class ChatbotState(TypedDict):
    messages: Annotated[list, add_messages(format="langchain-openai")]