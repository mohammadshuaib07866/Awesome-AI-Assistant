import streamlit as st

# Page Config
st.set_page_config(
    page_title="Awesome AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main Title
st.title("🤖 Awesome AI Assistant")

# ================= Sidebar =================
with st.sidebar:
    
    st.subheader("Chatbot")

    # New Chat Button
    if st.button("➕ New Chat"):
        st.session_state.messages = []

    st.divider()

    st.subheader("Recent Chats")

    # Static recent chats
    st.write("• Chat 1")
    st.write("• Chat 2")
    st.write("• Chat 3")

# ================= Chat Area =================

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_input = st.chat_input("Type here...")

# Add User Message
if user_input:
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Static Assistant Reply
    assistant_reply = "Hello! I am your AI Assistant."

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)