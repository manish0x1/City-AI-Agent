# 🏙️ City AI Agent

An AI-powered City Assistant built using **Python, Streamlit, LangChain, Mistral AI, Tavily Search, and OpenWeather API**. The assistant provides real-time weather updates and the latest city news with a Human-in-the-Loop (HITL) approval workflow.

---

## 🚀 Features

- 🌦️ Real-time Weather Information
- 📰 Latest City News using Tavily Search
- 🤖 AI-powered responses with Mistral AI
- ✅ Human-in-the-Loop Approval before tool execution
- 💬 Interactive Streamlit Chat UI
- 🔒 Secure API key management using `.env`

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- Tavily Search API
- OpenWeather API
- python-dotenv
- Requests

---

## 📂 Project Structure

```text
City-AI-Agent/
│── app.py
│── Agents.py
│── requirements.txt
│── .env
│── .gitignore
│── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/manish0x1/City-AI-Agent.git
cd City-AI-Agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💬 Example Prompts

- What is the weather in Jaipur?
- Show latest news about Mumbai.
- Weather in Delhi.
- Latest news in Bangalore.

---

## 🔒 Security

- Never upload your `.env` file.
- Keep your API keys private.
- Use `.gitignore` to exclude sensitive files.

---

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Submit a Pull Request.

---



## 👨‍💻 Author

**Manish Mahawar**

GitHub: https://github.com/manish0x1
