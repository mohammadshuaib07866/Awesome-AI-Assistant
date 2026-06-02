from langchain_core.messages import HumanMessage
from app.graph.builder import chatbot

import uuid
CONFIG = {"configurable": {"thread_id": str(uuid.uuid4())}}

print("Type your message and press Enter. Type 'quit' or 'exit' to stop.")

while True:
    user_text = input("You: ").strip()
    if user_text.lower() in {"quit", "exit", "q"}:
        print("Goodbye!")
        break

    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_text)
            ]
        },
        config=CONFIG
    )

    ai_response = response["messages"][-1].content
    print(f"AI: {ai_response}")
