# ✈️ AI Travel Booking System (Multi-Agent Architecture)

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://arpita-ai-travel.streamlit.app/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)](https://python.langchain.com/docs/langgraph)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20%7C%20LLaMA%203-8A2BE2?style=flat)](https://groq.com/)

A fully autonomous, multi-agent AI travel planner. Instead of relying on a single large language model to guess your itinerary, this application utilizes a sophisticated **LangGraph** architecture where four specialized AI agents collaborate in real-time to research, negotiate, and synthesize a complete travel plan.

🔗 **[Live Application](https://arpita-ai-travel.streamlit.app/)**

---

## 🧠 The Architecture (Agentic Workflow)

This system moves beyond simple generative text by employing task-specific agents that pass state and memory back and forth until the user's complex travel request is resolved.

1. ✈️ **Flight Agent:** Equipped with live aviation tools to pull real-time flight routes, pricing, and availability.
2. 🏨 **Hotel Agent:** Secures current accommodation metrics, ratings, and location data.
3. 🗓️ **Itinerary Agent:** Acts as the routing architect, taking raw data from the Flight and Hotel agents to build a logical, day-by-day schedule.
4. 🤖 **Final Agent:** The synthesizer. It reviews the entire LangGraph state, formats the final response, and generates a cohesive travel plan that can be exported directly to PDF or Markdown.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Custom Dark Mode UI)
* **Orchestration:** LangGraph (Stateful Multi-Agent Framework)
* **LLM:** LLaMA 3 (via Groq for ultra-low latency inference)
* **Database / Memory:** PostgreSQL (Hosted on Supabase for persistent thread checkpoints)
* **Tools:** Tavily Search API, AviationStack API
* **Export:** `xhtml2pdf`, `markdown`

---

## 🚀 Local Installation & Setup

If you want to run this multi-agent system on your local machine, follow these steps:

### 1. Prerequisites
* **Python 3.11** (Highly recommended for `pycairo` and PDF generation compatibility)
* A **Supabase** account (for PostgreSQL database)
* API Keys for **Groq**, **Tavily**, and **AviationStack**

### 2. Clone the Repository
```bash
git clone [https://github.com/imarpitajaiswal/ai-travel-planner.git](https://github.com/imarpitajaiswal/ai-travel-planner.git)
cd ai-travel-planner
