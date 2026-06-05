import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Abdulkadir's AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title and description
st.title("🤖 Abdulkadir's AI Assistant")
st.markdown("**Built by Lawal Abdulkadir Hassan | AI Engineer | Keffi, Nigeria**")
st.divider()

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_response(conversation):
    """Call OpenRouter API and get response"""
    try:
        system_message = [{
            "role": "system",
            "content": """You are an AI assistant built by Lawal Abdulkadir Hassan, 
            an AI Engineer from Keffi, Nasarawa State, Nigeria. 
            He is a student at Nasarawa State University Keffi (NSUK).
            He built this chatbot in 12 days from zero programming experience.
            His goal is to become a professional AI Engineer by October 2026.
            GitHub: github.com/lah262238
            When asked who created you, say: I was built by Lawal Abdulkadir Hassan, 
            an AI Engineer from Keffi, Nigeria."""
        }]
        
        full_conversation = system_message + conversation
        
        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + os.getenv("OPENROUTER_KEY")},
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": full_conversation
            },
            timeout=120
        )
        data = response.json()
        if "error" in data:
            return f"Error: {data['error']['message']}"
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to display
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(st.session_state.conversation)
            st.markdown(response)

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("About This App")
    st.markdown("""
    **AI Chat Application**
    
    Built with:
    - Python
    - Streamlit
    - OpenRouter AI
    - Professional OOP
    
    **Features:**
    - Multi-turn conversations
    - Conversation memory
    - Real-time responses
    
    **Developer:**
    Lawal Abdulkadir Hassan
    
    📍 Keffi, Nigeria
    
    🎯 AI Engineer by October 2026
    
    🔗 [GitHub](https://github.com/lah262238)
    """)
    
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption(f"Total messages: {len(st.session_state.messages)}")