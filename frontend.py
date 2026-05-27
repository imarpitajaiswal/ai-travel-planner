import os
import io
import markdown
from xhtml2pdf import pisa
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

st.set_page_config(page_title="AI Travel Booking System", page_icon="✈️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; background-color: #080d14; }
.hero-wrapper { position: relative; border-radius: 20px; overflow: hidden; margin-bottom: 2rem; height: 280px; }
.hero-bg { width: 100%; height: 100%; object-fit: cover; display: block; filter: brightness(0.35); position: absolute; top: 0; left: 0; }
.hero-content { position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem; }
.hero-badge { background: rgba(58,123,213,0.25); border: 1px solid rgba(58,123,213,0.5); color: #7ab8f5 !important; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.3rem 0.9rem; border-radius: 20px; margin-bottom: 0.9rem; display: inline-block; }
.hero-title { font-size: 2.6rem; font-weight: 700; color: #ffffff; margin: 0 0 0.6rem; line-height: 1.2; }
.hero-sub { color: #94adc8; font-size: 1rem; max-width: 560px; }
.input-label { color: #7ab8f5; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }
div[data-testid="stButton"] > button { background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 0.85rem 2.5rem !important; font-size: 1.05rem !important; font-weight: 700 !important; width: 100% !important; transition: all 0.3s ease !important; }
div[data-testid="stButton"] > button:hover { transform: translateY(-2px) !important; background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important; }
[data-testid="stStatusWidget"] { background: #0e1a2e !important; border: 1px solid #1e3050 !important; border-radius: 12px !important; }
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
.sec-head { display: flex; align-items: center; gap: 0.6rem; margin: 2rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #1e2e44; }
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }
.metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
.metric-box { flex: 1; background: #0e1623; border: 1px solid #1e2e44; border-radius: 12px; padding: 1rem 1.2rem; text-align: center; }
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { font-size: 0.78rem; color: #7aa8cc; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }
.final-card { background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%); border: 1px solid #1e3a5c; border-left: 4px solid #3a7bd5; border-radius: 14px; padding: 1.8rem; line-height: 1.8; color: #cce0f5; font-size: 0.95rem; }
section[data-testid="stSidebar"] { background: #090e18 !important; border-right: 1px solid #141f30 !important; }
.sidebar-chip { background: #0e1a2b; border: 1px solid #1a2e44; border-radius: 8px; padding: 0.45rem 0.75rem; margin-bottom: 0.4rem; font-size: 0.83rem; color: #7aa8cc; }
.sidebar-title { color: #e0edf8; font-size: 1rem; font-weight: 600; margin: 1rem 0 0.5rem; }
#MainMenu, footer, header { visibility: hidden; }
.stTextArea textarea { background: #0a1520 !important; border: 1px solid #1e2e44 !important; border-radius: 10px !important; color: #e8f4ff !important; font-size: 0.95rem !important; resize: none !important; }
input[type="text"], .stTextInput input { background: #0e1a2b !important; border: 1px solid #1a2e44 !important; border-radius: 8px !important; color: #e0edf8 !important; }
.stMarkdown p, .stMarkdown li { color: #cce0f5 !important; }

/* Custom CSS to make BOTH download buttons look identical with the blue gradient */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    thread_id = st.text_input("👤 User ID", value="user_arpita",
                              help="Your session ID — keeps travel history across queries")

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg" src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"/>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ AI Travel Booking System</div>
        <div class="hero-sub">Four specialized agents work together to deliver your perfect trip plan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)
user_query = st.text_area(label="Trip Description", placeholder="e.g. Plan a 7-day Japan trip including flights and hotels...", height=100, label_visibility="collapsed")
generate = st.button("🚀 Generate My Travel Plan", use_container_width=True)

AGENT_META = {
    "flight_agent": ("✈️", "Flight Agent"),
    "hotel_agent": ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent": ("🧠", "Final Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "", "itinerary": "", "final_response": "", "llm_calls": 0}

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>", unsafe_allow_html=True)

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))
                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")
                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")
                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")
                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")
                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """, unsafe_allow_html=True)

        if collected["final_response"]:
            st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='final-card'>{collected['final_response']}</div>", unsafe_allow_html=True)

        # 1. Save Markdown File Locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_md = f"travel_plan_{timestamp}.md"
        filename_pdf = f"travel_plan_{timestamp}.pdf"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan\n**Query:** {user_query}\n**User ID:** {thread_id}\n\n---\n{collected['final_response']}"""
        
        with open(os.path.join(save_dir, filename_md), "w", encoding="utf-8") as f:
            f.write(file_content)

        # 2. Helper function to generate styled PDF from Markdown
        def generate_pdf(md_text):
            html_content = markdown.markdown(md_text)
            styled_html = f"""
            <html>
            <head>
            <style>
                @page {{ margin: 2cm; }}
                body {{ font-family: Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.6; font-size: 12px; }}
                h1 {{ color: #0d4a8a; font-size: 24px; border-bottom: 2px solid #1a6bbf; padding-bottom: 5px; }}
                h2 {{ color: #1a6bbf; font-size: 18px; margin-top: 20px; }}
                h3 {{ color: #333333; font-size: 14px; }}
                hr {{ border: 0.5px solid #dddddd; margin: 15px 0; }}
                li {{ margin-bottom: 5px; }}
            </style>
            </head>
            <body>
            {html_content}
            </body>
            </html>
            """
            pdf_buffer = io.BytesIO()
            pisa.CreatePDF(io.StringIO(styled_html), dest=pdf_buffer)
            return pdf_buffer.getvalue()

        # 3. Create three columns for Markdown, PDF, and the Auto-save path
        dl_md_col, dl_pdf_col, info_col = st.columns([1, 1, 2], vertical_alignment="center")
        
        with dl_md_col:
            st.download_button(
                label="⬇️ Markdown", 
                data=file_content, 
                file_name=filename_md, 
                mime="text/markdown", 
                use_container_width=True,
                key="download_md_btn"
            )
        
        with dl_pdf_col:
            pdf_bytes = generate_pdf(file_content)
            st.download_button(
                label="📄 PDF Plan", 
                data=pdf_bytes, 
                file_name=filename_pdf, 
                mime="application/pdf", 
                use_container_width=True,
                key="download_pdf_btn"
            )
            
        with info_col:
            st.markdown(f"""
            <div class="save-bar" style="display: flex; align-items: center; justify-content: flex-start; margin-top: 0; height: 100%;">
                📁 Auto-saved → <code style="margin-left: 8px; background: #0a1520; color: #7ab8f5; padding: 0.15rem 0.4rem; border-radius: 4px;">travel_plans/{filename_md}</code>
            </div>
            """, unsafe_allow_html=True)