import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tavily import TavilyClient

# Load Environment Variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="City Assistant", page_icon="🏙️", layout="centered")
st.title("🏙️ AI City Assistant")
st.caption("Weather aur News check karein human-in-the-loop approval ke sath.")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_tool_call" not in st.session_state:
    st.session_state.pending_tool_call = None

# =========================
# 🌦️ Weather Tool
# =========================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://openweathermap.org{city},IN&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if str(data.get("cod")) != "200":
            return f"Error: {data.get('message', 'Could not fetch weather')}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {desc}, {temp}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# =========================
# 📰 News Tool (Tavily)
# =========================
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    try:
        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=3
        )
        results = response.get("results", [])
        if not results:
            return f"No news found for {city}"
        
        news_list = []
        for r in results:
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("content", "")
            news_list.append(f"- **{title}**\n  🔗 {url}\n  📝 {snippet[:100]}...")
        return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)
    except Exception as e:
        return f"Error fetching news: {str(e)}"

# Tools Dictionary mapping
tools_map = {"get_weather": get_weather, "get_news": get_news}

# =========================
# 🧠 LLM Setup
# =========================
llm = ChatMistralAI(model="mistral-small-2506").bind_tools([get_weather, get_news])

# Previous Messages Render Karein
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        st.chat_message("assistant").write(msg.content)

# User Input
if user_input := st.chat_input("Ask about a city (e.g., 'What is the weather in Mumbai?')"):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # LLM Call
    with st.spinner("Thinking..."):
        system_msg = HumanMessage(content="System: You are a helpful city assistant.")
        response = llm.invoke([system_msg] + st.session_state.messages)
    
    # Check if tool call is requested
    if response.tool_calls:
        st.session_state.pending_tool_call = response.tool_calls[0] # Handle single tool call
        st.session_state.messages.append(response)
        st.rerun()
    else:
        st.chat_message("assistant").write(response.content)
        st.session_state.messages.append(response)

# =========================
# 🎛️ Human-in-the-Loop UI
# =========================
if st.session_state.pending_tool_call:
    tool_call = st.session_state.pending_tool_call
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    
    st.warning(f"🤖 Agent wants to call tool: **{tool_name}** with arguments: `{tool_args}`")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Approve", use_container_width=True):
            with st.spinner("Running tool..."):
                # Execute tool
                selected_tool = tools_map[tool_name]
                tool_output = selected_tool.invoke(tool_args)
                
                # Append Tool result to history
                st.session_state.messages.append(
                    ToolMessage(content=tool_output, tool_call_id=tool_call["id"])
                )
                
                # Get final answer from LLM
                system_msg = HumanMessage(content="System: You are a helpful city assistant.")
                final_response = llm.invoke([system_msg] + st.session_state.messages)
                st.session_state.messages.append(final_response)
                
                # Reset state and refresh
                st.session_state.pending_tool_call = None
                st.rerun()
                
    with col2:
        if st.button("❌ Deny", use_container_width=True):
            st.session_state.messages.append(
                ToolMessage(content="Tool call denied by user.", tool_call_id=tool_call["id"])
            )
            # Ask LLM to respond to denial
            system_msg = HumanMessage(content="System: You are a helpful city assistant.")
            final_response = llm.invoke([system_msg] + st.session_state.messages)
            st.session_state.messages.append(final_response)
            
            st.session_state.pending_tool_call = None
            st.rerun()
