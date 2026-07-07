from dotenv import load_dotenv
import os
import requests
import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent

load_dotenv()

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="🌍 City AI Agent",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------

st.markdown("""
<style>

.main{
    padding-top:1rem;
}

h1{
    text-align:center;
}

.block-container{
    padding-top:2rem;
}

.chat-message{
    padding:12px;
    border-radius:12px;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

div[data-testid="stSidebar"]{
    background:#111827;
}

.footer{
text-align:center;
color:gray;
padding-top:20px;
}

.example{
background:#f4f4f4;
padding:10px;
border-radius:10px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Weather Tool
# ----------------------------

@tool
def get_weather(city: str) -> str:
    """Get current weather"""

    api_key=os.getenv("OPENWEATHER_API_KEY")

    url=f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"

    data=requests.get(url).json()

    if str(data.get("cod"))!="200":
        return "Weather not found."

    temp=data["main"]["temp"]
    desc=data["weather"][0]["description"]

    return f"""
## 🌦 Weather Report

**City :** {city}

**Temperature :** {temp}°C

**Condition :** {desc}
"""

# ----------------------------
# News Tool
# ----------------------------

tavily_client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city:str)->str:
    """Get latest news"""

    response=tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results=response.get("results",[])

    if len(results)==0:
        return "No News Found."

    output="## 📰 Latest News\n\n"

    for i,r in enumerate(results,1):

        output+=f"""
### {i}. {r['title']}

{r['content'][:180]}...

🔗 {r['url']}

---
"""

    return output

# ----------------------------
# LLM
# ----------------------------

llm=ChatMistralAI(
    model="mistral-small-2506"
)

agent=create_agent(
    llm,
    tools=[get_weather,get_news],
    system_prompt="""
You are a smart AI City Assistant.

You can

- Weather
- Latest News

Always answer beautifully using markdown.
"""
)

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("🌍 City AI Agent")

    st.write("---")

    st.success("Powered by")

    st.write("✅ Mistral AI")

    st.write("✅ LangChain")

    st.write("✅ Tavily")

    st.write("✅ OpenWeather")

    st.write("---")

    st.subheader("💡 Example Questions")

    st.markdown("""
- Weather in Jaipur

- Latest News in Delhi

- News in Mumbai

- Weather in Bangalore

- Latest news in Kota
""")

    st.write("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

# ----------------------------
# Header
# ----------------------------

st.title("🌍 City AI Assistant")

st.caption("Get Weather & Latest News using AI")

st.write("")

# ----------------------------
# Session
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages=[]

# ----------------------------
# Display Messages
# ----------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Chat
# ----------------------------

question=st.chat_input("Ask anything about a city...")

if question:

    st.session_state.messages.append({
        "role":"user",
        "content":question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            response=agent.invoke({
                "messages":[
                    {
                        "role":"user",
                        "content":question
                    }
                ]
            })

            answer=response["messages"][-1].content

            st.markdown(answer)

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer
    })

st.write("---")

st.markdown(
    "<div class='footer'>Made with ❤️ using LangChain + Mistral AI + Streamlit</div>",
    unsafe_allow_html=True
)