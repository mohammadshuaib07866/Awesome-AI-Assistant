from langchain_core.messages import HumanMessage
from app.graph.builder import chatbot

import uuid


CONFIG = {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    }
}


print("Type your message and press Enter.")
print("Type 'quit' or 'exit' to stop.\n")


while True:

    user_text = input("You: ").strip()

    if user_text.lower() in {"quit", "exit", "q"}:
        print("Goodbye!")
        break

    print("AI: ", end="", flush=True)

    for message_chunk, metadata in chatbot.stream(
        {
            "messages": [
                HumanMessage(content=user_text)
            ]
        },
        config=CONFIG,
        stream_mode="messages"
    ):

        if message_chunk.content:
            print(message_chunk.content, end="", flush=True)

    print("\n")