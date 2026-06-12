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
st.markdown("✨ **Now with Real-Time Google Search!**")
st.divider()

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "search_enabled" not in st.session_state:
    st.session_state.search_enabled = True


def search_tavily(query):
    """Search using Tavily API for real-time current information"""
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return None
        
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "max_results": 5,
                "include_answer": True
            },
            timeout=10
        )
        
        data = response.json()
        
        if not data.get('results'):
            return None
        
        # Format search results
        search_summary = "**🔍 Real-Time Search Results:**\n\n"
        
        # Add AI-generated answer if available
        if data.get('answer'):
            search_summary += f"**💡 Quick Answer:** {data['answer']}\n\n"
        
        search_summary += "**📰 Sources:**\n"
        for i, result in enumerate(data.get('results', [])[:3], 1):
            title = result.get('title', 'No title')
            body = result.get('content', 'No description')[:150]
            link = result.get('url', '#')
            search_summary += f"{i}. **{title}**\n{body}...\n[Read more]({link})\n\n"
        
        return search_summary
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return None


def should_search(user_message):
    """Determine if this query needs real-time information"""
    search_keywords = [
        "current", "today", "latest", "now", "right now",
        "2024", "2025", "2026", "recent", "breaking",
        "news", "weather", "price", "stock", "live",
        "what is the date", "who is", "where is",
        "what happened", "how many", "statistics",
        "president", "prime minister", "latest news",
        "this week", "this month", "this year",
        "today's", "yesterday", "tomorrow"
    ]
    
    message_lower = user_message.lower()
    return any(keyword in message_lower for keyword in search_keywords)


def get_ai_response(conversation, search_results=None):
    """Call OpenRouter API and get response"""
    try:
        system_message = [{
            "role": "system",
            "content": """You are an AI assistant built by Lawal Abdulkadir Hassan, 
            an AI Engineer from Keffi, Nasarawa State, Nigeria. 
            He is a student at Nasarawa State University Keffi (NSUK).
            He built this chatbot in 16 days from zero programming experience.
            His goal is to become a professional AI Engineer by October 2026.
            GitHub: github.com/lah262238
            
            When asked who created you, say: I was built by Lawal Abdulkadir Hassan, 
            an AI Engineer from Keffi, Nigeria.
            
            You have access to real-time information from the internet.
            When search results are provided, use them to give accurate, current information.
            Always cite sources when using search results."""
        }]
        
        # Add search results to context if available
        if search_results:
            search_context = [{
                "role": "system",
                "content": f"Here is current information from the internet:\n\n{search_results}\n\nUse this information to answer the user's question accurately."
            }]
            full_conversation = system_message + search_context + conversation
        else:
            full_conversation = system_message + conversation
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + os.getenv("OPENROUTER_KEY")},
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": full_conversation,
                "temperature": 0.7
            },
            timeout=120,
            verify=False
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


# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.search_enabled = st.toggle(
        "🔍 Enable Real-Time Search",
        value=True,
        help="Search the internet for current information"
    )
    
    st.divider()
    
    st.header("About This App")
    st.markdown("""
    **AI Chat Application v2.0**
    
    Built with:
    - Python
    - Streamlit
    - OpenRouter AI
    - Tavily Search API
    
    **Features:**
    - 💬 Multi-turn conversations
    - 🧠 Conversation memory
    - ⚡ Real-time responses
    - 🔍 Real-time internet search
    - 📰 Current news & information
    - 📊 Always up-to-date
    
    **Developer:**
    Lawal Abdulkadir Hassan
    
    📍 Keffi, Nigeria
    🎯 AI Engineer by October 2026
    🔗 [GitHub](https://github.com/lah262238)
    """)
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption(f"📊 Total messages: {len(st.session_state.messages)}")


# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to display
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response with optional search
    with st.chat_message("assistant"):
        search_results = None
        
        # Check if we should search for this query
        if st.session_state.search_enabled and should_search(prompt):
            with st.spinner("🔍 Searching the internet for current information..."):
                search_results = search_tavily(prompt)
                
                # Show search results if found
                if search_results:
                    with st.expander("📰 View Search Results"):
                        st.markdown(search_results)
        
        # Get AI response (with search context if available)
        with st.spinner("🤖 Thinking..."):
            response = get_ai_response(st.session_state.conversation, search_results)
            st.markdown(response)

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation.append({"role": "assistant", "content": response})


# Footer
st.divider()
st.caption("🚀 Powered by AI | Built in Nigeria | Made with ❤️ by Lawal Abdulkadir Hassan")