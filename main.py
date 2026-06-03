import streamlit as st
import uuid

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.graph.builder import chatbot
from app.graph.builder import retrieve_all_threads

# ==============================
# Generate Thread ID
# ==============================


def generate_thread_id():
    return str(uuid.uuid4())


# ==============================
# Utility Functions
# ==============================


def add_thread(thread_id, title=None):

    existing_thread_ids = [
        chat["thread_id"] for chat in st.session_state["chat_threads"]
    ]

    if title is None:
        base_title = "New Chat"
        title = base_title
        existing_titles = {chat["title"] for chat in st.session_state["chat_threads"]}
        counter = 1

        while title in existing_titles:
            counter += 1
            title = f"{base_title} {counter}"

    if thread_id not in existing_thread_ids:

        st.session_state["chat_threads"].append(
            {"thread_id": thread_id, "title": title}
        )


def reset_chat():

    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id

    add_thread(thread_id)

    st.session_state["message_history"] = []


def load_conversation(thread_id):

    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})

    return state.values.get("messages", [])


# ==============================
# Page Config
# ==============================

st.set_page_config(page_title="Awesome AI Assistant", page_icon="🤖", layout="wide")

# ==============================
# Initialize Session State
# ==============================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads() or []

add_thread(st.session_state["thread_id"])


# ==============================
# Main Title
# ==============================

st.title("🤖 Awesome AI Assistant")


# ==============================
# Sidebar
# ==============================

with st.sidebar:

    st.subheader("Chatbot")

    # New Chat Button
    if st.button("➕ New Chat"):

        reset_chat()

        st.rerun()

    st.divider()

    st.subheader("Recent Chats")

    # Show Chat Threads
    for chat in st.session_state["chat_threads"][::-1]:

        thread_id = chat["thread_id"]

        title = chat["title"]

        if st.button(title, key=f"thread-{thread_id}"):

            st.session_state["thread_id"] = thread_id

            messages = load_conversation(thread_id)

            temp_messages = []

            for msg in messages:

                if isinstance(msg, HumanMessage):

                    role = "user"

                elif isinstance(msg, AIMessage):

                    role = "assistant"

                else:
                    continue

                temp_messages.append({"role": role, "content": msg.content})

            st.session_state["message_history"] = temp_messages

            st.rerun()

    st.divider()


# ==============================
# Display Old Messages
# ==============================

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==============================
# Chat Input
# ==============================

user_input = st.chat_input("Type here...")


# ==============================
# Handle User Input
# ==============================

if user_input:

    # ==============================
    # Auto Set Chat Title
    # ==============================

    current_thread = next(
        (
            chat
            for chat in st.session_state["chat_threads"]
            if chat["thread_id"] == st.session_state["thread_id"]
        ),
        None,
    )

    # First question becomes title
    if current_thread and current_thread["title"] == "New Chat":

        title = user_input.strip()

        # Limit Title Length
        if len(title) > 35:
            title = title[:35] + "..."

        current_thread["title"] = title

    # ==============================
    # Save User Message
    # ==============================

    st.session_state["message_history"].append({"role": "user", "content": user_input})

    # Display User Message
    with st.chat_message("user"):

        st.markdown(user_input)

    # ==============================
    # Assistant Response
    # ==============================

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        # Streaming Generator
        def response_generator():

            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": st.session_state["thread_id"]}},
                stream_mode="messages",
            ):

                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"Using `{tool_name}`---", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            f"Using `{tool_name}` ---", state="running", expanded=True
                        )
                if message_chunk.content:
                    yield message_chunk.content

        # Stream AI Response
        ai_message = st.write_stream(response_generator())

        if isinstance(ai_message, (list, tuple)):
            ai_message = "".join(str(chunk) for chunk in ai_message)
        elif ai_message is None:
            ai_message = ""
        else:
            ai_message = str(ai_message)

        ## Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="Tool finished", state="complete", expanded=False
            )

    # ==============================
    # Save Assistant Response
    # ==============================

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
