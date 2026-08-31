# import streamlit as st
# import time
# from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# # ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="ResearchMind · AI Research Agent",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

# /* ── Reset & base ── */
# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif;
#     color: #e8e4dc;
# }

# .stApp {
#     background: #0a0a0f;
#     background-image:
#         radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
#         radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
# }

# /* ── Hide default streamlit chrome ── */
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

# /* ── Hero header ── */
# .hero {
#     text-align: center;
#     padding: 3.5rem 0 2.5rem;
#     position: relative;
# }
# .hero-eyebrow {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.7rem;
#     font-weight: 500;
#     letter-spacing: 0.25em;
#     text-transform: uppercase;
#     color: #ff8c32;
#     margin-bottom: 1rem;
#     opacity: 0.9;
# }
# .hero h1 {
#     font-family: 'Syne', sans-serif;
#     font-size: clamp(2.8rem, 6vw, 5rem);
#     font-weight: 800;
#     line-height: 1.0;
#     letter-spacing: -0.03em;
#     color: #f0ebe0;
#     margin: 0 0 1rem;
# }
# .hero h1 span {
#     color: #ff8c32;
# }
# .hero-sub {
#     font-size: 1.05rem;
#     font-weight: 300;
#     color: #a09890;
#     max-width: 520px;
#     margin: 0 auto;
#     line-height: 1.65;
# }

# /* ── Divider ── */
# .divider {
#     height: 1px;
#     background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
#     margin: 2rem 0;
# }

# /* ── Input card ── */
# .input-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,140,50,0.15);
#     border-radius: 16px;
#     padding: 2rem 2.5rem;
#     margin-bottom: 2rem;
#     backdrop-filter: blur(8px);
# }

# /* ── Streamlit input overrides ── */
# .stTextInput > div > div > input {
#     background: rgba(255,255,255,0.05) !important;
#     border: 1px solid rgba(255,140,50,0.25) !important;
#     border-radius: 10px !important;
#     color: #f0ebe0 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 1rem !important;
#     padding: 0.75rem 1rem !important;
#     transition: border-color 0.2s, box-shadow 0.2s !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: #ff8c32 !important;
#     box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
# }
# .stTextInput > label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.72rem !important;
#     letter-spacing: 0.15em !important;
#     text-transform: uppercase !important;
#     color: #ff8c32 !important;
#     font-weight: 500 !important;
# }

# /* ── Button ── */
# .stButton > button {
#     background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
#     color: #0a0a0f !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.95rem !important;
#     letter-spacing: 0.04em !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.7rem 2.2rem !important;
#     cursor: pointer !important;
#     transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
#     box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
#     width: 100%;
# }
# .stButton > button:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
#     opacity: 0.95 !important;
# }
# .stButton > button:active {
#     transform: translateY(0) !important;
# }

# /* ── Pipeline step cards ── */
# .step-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 14px;
#     padding: 1.5rem 1.8rem;
#     margin-bottom: 1.2rem;
#     position: relative;
#     overflow: hidden;
#     transition: border-color 0.3s;
# }
# .step-card.active {
#     border-color: rgba(255,140,50,0.4);
#     background: rgba(255,140,50,0.04);
# }
# .step-card.done {
#     border-color: rgba(80,200,120,0.3);
#     background: rgba(80,200,120,0.03);
# }
# .step-card::before {
#     content: '';
#     position: absolute;
#     left: 0; top: 0; bottom: 0;
#     width: 3px;
#     border-radius: 14px 0 0 14px;
#     background: rgba(255,255,255,0.05);
#     transition: background 0.3s;
# }
# .step-card.active::before { background: #ff8c32; }
# .step-card.done::before   { background: #50c878; }

# .step-header {
#     display: flex;
#     align-items: center;
#     gap: 0.8rem;
#     margin-bottom: 0.3rem;
# }
# .step-num {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.68rem;
#     font-weight: 500;
#     letter-spacing: 0.15em;
#     color: #ff8c32;
#     opacity: 0.7;
# }
# .step-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 0.95rem;
#     font-weight: 700;
#     color: #f0ebe0;
# }
# .step-status {
#     margin-left: auto;
#     font-family: 'DM Mono', monospace;
#     font-size: 0.68rem;
#     letter-spacing: 0.1em;
# }
# .status-waiting  { color: #555; }
# .status-running  { color: #ff8c32; }
# .status-done     { color: #50c878; }

# /* ── Result panels ── */
# .result-panel {
#     background: rgba(255,255,255,0.025);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 14px;
#     padding: 1.8rem 2rem;
#     margin-top: 1rem;
#     margin-bottom: 1.5rem;
# }
# .result-panel-title {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.7rem;
#     font-weight: 500;
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     color: #ff8c32;
#     margin-bottom: 1rem;
#     padding-bottom: 0.7rem;
#     border-bottom: 1px solid rgba(255,140,50,0.15);
# }
# .result-content {
#     font-size: 0.92rem;
#     line-height: 1.8;
#     color: #cdc8bf;
#     white-space: pre-wrap;
#     font-family: 'DM Sans', sans-serif;
# }

# /* ── Report & feedback panels ── */
# .report-panel {
#     background: rgba(255,255,255,0.025);
#     border: 1px solid rgba(255,140,50,0.2);
#     border-radius: 16px;
#     padding: 2rem 2.5rem;
#     margin-top: 1rem;
# }
# .feedback-panel {
#     background: rgba(255,255,255,0.025);
#     border: 1px solid rgba(80,200,120,0.2);
#     border-radius: 16px;
#     padding: 2rem 2.5rem;
#     margin-top: 1rem;
# }
# .panel-label {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.7rem;
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     margin-bottom: 1.2rem;
#     padding-bottom: 0.7rem;
# }
# .panel-label.orange {
#     color: #ff8c32;
#     border-bottom: 1px solid rgba(255,140,50,0.15);
# }
# .panel-label.green {
#     color: #50c878;
#     border-bottom: 1px solid rgba(80,200,120,0.15);
# }

# /* ── Progress text ── */
# .stSpinner > div { color: #ff8c32 !important; }

# /* ── Expander ── */
# details summary {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.75rem !important;
#     color: #a09890 !important;
#     letter-spacing: 0.1em !important;
#     cursor: pointer;
# }

# /* ── Section heading ── */
# .section-heading {
#     font-family: 'Syne', sans-serif;
#     font-size: 1.3rem;
#     font-weight: 700;
#     color: #f0ebe0;
#     margin: 2rem 0 1rem;
# }

# /* ── Toast-style notice ── */
# .notice {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.72rem;
#     color: #605850;
#     text-align: center;
#     margin-top: 3rem;
#     letter-spacing: 0.08em;
# }
# </style>
# """, unsafe_allow_html=True)


# # ── Helper: render a step card ────────────────────────────────────────────────
# def step_card(num: str, title: str, state: str, desc: str = ""):
#     status_map = {
#         "waiting": ("WAITING", "status-waiting"),
#         "running": ("● RUNNING", "status-running"),
#         "done":    ("✓ DONE",   "status-done"),
#     }
#     label, cls = status_map.get(state, ("", ""))
#     card_cls = {"running": "active", "done": "done"}.get(state, "")
#     st.markdown(f"""
#     <div class="step-card {card_cls}">
#         <div class="step-header">
#             <span class="step-num">{num}</span>
#             <span class="step-title">{title}</span>
#             <span class="step-status {cls}">{label}</span>
#         </div>
#         {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
#     </div>
#     """, unsafe_allow_html=True)


# # ── Session state init ────────────────────────────────────────────────────────
# for key in ("results", "running", "done"):
#     if key not in st.session_state:
#         st.session_state[key] = {} if key == "results" else False


# # ── Hero ──────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <div class="hero-eyebrow">Multi-Agent AI System</div>
#     <h1>Research<span>Mind</span></h1>
#     <p class="hero-sub">
#         Four specialized AI agents collaborate — searching, scraping, writing,
#         and critiquing — to deliver a polished research report on any topic.
#     </p>
# </div>
# <div class="divider"></div>
# """, unsafe_allow_html=True)


# # ── Layout: input left, pipeline right ───────────────────────────────────────
# col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

# with col_input:
#     st.markdown('<div class="input-card">', unsafe_allow_html=True)
#     topic = st.text_input(
#         "Research Topic",
#         placeholder="e.g. Quantum computing breakthroughs in 2025",
#         key="topic_input",
#         label_visibility="visible",
#     )
#     run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Example chips
#     st.markdown("""
#     <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
#         <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
#     """, unsafe_allow_html=True)
#     examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
#     for ex in examples:
#         st.markdown(f"""
#         <span style="
#             background:rgba(255,255,255,0.04);
#             border:1px solid rgba(255,255,255,0.08);
#             border-radius:6px;
#             padding:0.25rem 0.7rem;
#             font-size:0.75rem;
#             color:#a09890;
#             font-family:'DM Sans',sans-serif;
#             cursor:default;
#         ">{ex}</span>
#         """, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

# with col_pipeline:
#     st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

#     r = st.session_state.results
#     done = st.session_state.done

#     def s(step):
#         if not r:
#             return "waiting"
#         steps = ["search", "reader", "writer", "critic"]
#         idx = steps.index(step)
#         completed = list(r.keys())
#         # figure out which steps are done
#         if step in r:
#             return "done"
#         # which step is running now (first not in r)
#         if st.session_state.running:
#             for i, k in enumerate(steps):
#                 if k not in r:
#                     return "running" if k == step else "waiting"
#         return "waiting"

#     step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
#     step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
#     step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
#     step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# # ── Run pipeline ──────────────────────────────────────────────────────────────
# if run_btn:
#     if not topic.strip():
#         st.warning("Please enter a research topic first.")
#     else:
#         st.session_state.results = {}
#         st.session_state.running = True
#         st.session_state.done = False
#         st.rerun()

# if st.session_state.running and not st.session_state.done:
#     results = {}
#     topic_val = st.session_state.topic_input

#     # ── Step 1: Search ──
#     with st.spinner("🔍  Search Agent is working…"):
#         search_agent = build_search_agent()
#         sr = search_agent.invoke({
#             "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
#         })
#         results["search"] = sr["messages"][-1].content
#         st.session_state.results = dict(results)
#     st.rerun() if False else None   # keep inline for now

#     # ── Step 2: Reader ──
#     with st.spinner("📄  Reader Agent is scraping top resources…"):
#         reader_agent = build_reader_agent()
#         rr = reader_agent.invoke({
#             "messages": [("user",
#                 f"Based on the following search results about '{topic_val}', "
#                 f"pick the most relevant URL and scrape it for deeper content.\n\n"
#                 f"Search Results:\n{results['search'][:800]}"
#             )]
#         })
#         results["reader"] = rr["messages"][-1].content
#         st.session_state.results = dict(results)

#     # ── Step 3: Writer ──
#     with st.spinner("✍️  Writer is drafting the report…"):
#         research_combined = (
#             f"SEARCH RESULTS:\n{results['search']}\n\n"
#             f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
#         )
#         results["writer"] = writer_chain.invoke({
#             "topic": topic_val,
#             "research": research_combined
#         })
#         st.session_state.results = dict(results)

#     # ── Step 4: Critic ──
#     with st.spinner("🧐  Critic is reviewing the report…"):
#         results["critic"] = critic_chain.invoke({
#             "report": results["writer"]
#         })
#         st.session_state.results = dict(results)

#     st.session_state.running = False
#     st.session_state.done = True
#     st.rerun()


# # ── Results display ───────────────────────────────────────────────────────────
# r = st.session_state.results

# if r:
#     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

#     # Raw outputs in expanders
#     if "search" in r:
#         with st.expander("🔍 Search Results (raw)", expanded=False):
#             st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
#                         f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

#     if "reader" in r:
#         with st.expander("📄 Scraped Content (raw)", expanded=False):
#             st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
#                         f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

#     # Final report
#     if "writer" in r:
#         st.markdown("""
#         <div class="report-panel">
#             <div class="panel-label orange">📝 Final Research Report</div>
#         """, unsafe_allow_html=True)
#         st.markdown(r["writer"])   # render markdown natively
#         st.markdown("</div>", unsafe_allow_html=True)

#         # Download
#         st.download_button(
#             label="⬇  Download Report (.md)",
#             data=r["writer"],
#             file_name=f"research_report_{int(time.time())}.md",
#             mime="text/markdown",
#         )

#     # Critic feedback
#     if "critic" in r:
#         st.markdown("""
#         <div class="feedback-panel">
#             <div class="panel-label green">🧐 Critic Feedback</div>
#         """, unsafe_allow_html=True)
#         st.markdown(r["critic"])
#         st.markdown("</div>", unsafe_allow_html=True)


# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="notice">
#     ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
# </div>
# """, unsafe_allow_html=True)

#======================================================================
import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Studio Workspace",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (High-Contrast Light Theme + Fixed Container Panels) ──────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* ── Global Text & Colors ── */
html, body, [class*="css"], .stMarkdown, p, span, label, div {
    font-family: 'Inter', sans-serif;
    color: #000000 !important;
}

.stApp {
    background-color: #f1f5f9;
}

/* ── Fix Streamlit Header & Sidebar Re-open Toggle ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent !important;
}

button[data-testid="stSidebarCollapseButton"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stHeader"] button {
    color: #000000 !important;
    visibility: visible !important;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1.5px solid #cbd5e1;
    padding-top: 1rem;
}

.sidebar-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #000000 !important;
    margin-bottom: 0.2rem;
}

.sidebar-sub {
    font-size: 0.8rem;
    color: #334155 !important;
    margin-bottom: 1.5rem;
}

/* ── Form Controls Overrides ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #64748b !important;
    border-radius: 8px !important;
    color: #000000 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 0.85rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
}

.stTextInput > label {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Primary Button Styling */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.25rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3) !important;
    width: 100%;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px);
}

.stButton > button:disabled {
    background: #93c5fd !important;
    color: #ffffff !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

.stButton > button * {
    color: #ffffff !important;
}

/* ── Sidebar Progress Timeline ── */
.timeline-container {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1.5px solid #cbd5e1;
}

.timeline-item {
    position: relative;
    padding-left: 2rem;
    padding-bottom: 1.2rem;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: 0.45rem;
    top: 1.2rem;
    bottom: 0;
    width: 2px;
    background: #cbd5e1;
}

.timeline-item:last-child::before {
    display: none;
}

.timeline-dot {
    position: absolute;
    left: 0;
    top: 0.15rem;
    width: 1rem;
    height: 1rem;
    border-radius: 50%;
    background: #94a3b8;
    border: 2px solid #ffffff;
    box-shadow: 0 0 0 2px #cbd5e1;
}

.timeline-item.running .timeline-dot {
    background: #2563eb;
    box-shadow: 0 0 0 3px #93c5fd;
}

.timeline-item.done .timeline-dot {
    background: #16a34a;
    box-shadow: 0 0 0 3px #86efac;
}

.timeline-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #000000 !important;
}

.timeline-status {
    font-size: 0.775rem;
    font-weight: 600;
    color: #334155 !important;
    margin-top: 0.1rem;
}

.status-running { color: #1d4ed8 !important; }
.status-done { color: #15803d !important; }

/* ── Content Studio Canvas Cards ── */
.canvas-header {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.canvas-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #000000 !important;
}

/* Target Streamlit containers directly inside tabs to create solid white cards */
div[data-testid="stTabPanel"] > div {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 2.5rem 3rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    min-height: 450px !important;
    margin-top: 1rem !important;
}

/* ── Metric Box ── */
.metric-box {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #1d4ed8 !important;
}

.metric-lbl {
    font-size: 0.75rem;
    font-weight: 700;
    color: #334155 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Tabs Override ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #cbd5e1;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #475569 !important;
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    color: #1d4ed8 !important;
    font-weight: 700;
    border-bottom: 3px solid #1d4ed8;
}

/* ── Download Button Override ── */
.stDownloadButton > button {
    background: #ffffff !important;
    border: 1.5px solid #000000 !important;
    color: #000000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
}

.stDownloadButton > button:hover {
    background: #f1f5f9 !important;
    border-color: #2563eb !important;
    color: #2563eb !important;
}

.stDownloadButton > button * {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ─────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "current_step" not in st.session_state:
    st.session_state.current_step = None


# ── Dynamic Button Label & Disabled State Mapping ───────────────────────────
step_button_labels = {
    "search": "⏳ Step 1/4: Searching Web...",
    "reader": "⏳ Step 2/4: Scraping Sources...",
    "writer": "⏳ Step 3/4: Drafting Report...",
    "critic": "⏳ Step 4/4: Reviewing Quality...",
}

is_processing = st.session_state.current_step in step_button_labels
button_text = step_button_labels.get(st.session_state.current_step, "Start Pipeline")


# ── Sidebar Control Center ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">ResearchMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Studio Edition · Multi-Agent Control</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Target",
        placeholder="e.g. LLM agents 2026",
        key="topic_input",
        disabled=is_processing
    )

    run_btn = st.button(
        button_text, 
        use_container_width=True, 
        disabled=is_processing
    )

    st.markdown("---")
    st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#000000; margin-bottom:0.5rem;'>QUICK TEMPLATES</div>", unsafe_allow_html=True)
    
    presets = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress"]
    for p in presets:
        st.markdown(f"<span style='font-size:0.85rem; font-weight:500; color:#000000;'>• {p}</span>", unsafe_allow_html=True)

    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#000000; margin-bottom:1rem;'>LIVE AGENT TIMELINE</div>", unsafe_allow_html=True)

    r = st.session_state.results
    c_step = st.session_state.current_step

    def get_step_state(step_name):
        if step_name in r:
            return "done"
        if c_step == step_name:
            return "running"
        return "waiting"

    def render_timeline_item(title, state, desc):
        status_labels = {
            "waiting": ("Idle", ""), 
            "running": ("ACTIVE NOW", "status-running"), 
            "done": ("COMPLETE", "status-done")
        }
        label, cls = status_labels.get(state, ("Idle", ""))
        st.markdown(f"""
        <div class="timeline-item {state}">
            <div class="timeline-dot"></div>
            <div class="timeline-title">{title}</div>
            <div class="timeline-status {cls}"><b>[{label}]</b> {desc}</div>
        </div>
        """, unsafe_allow_html=True)

    render_timeline_item("1. Search Agent", get_step_state("search"), "Queries web sources")
    render_timeline_item("2. Reader Agent", get_step_state("reader"), "Parses deep content")
    render_timeline_item("3. Writer Chain", get_step_state("writer"), "Drafts document")
    render_timeline_item("4. Critic Chain", get_step_state("critic"), "Evaluates precision")

    st.markdown('</div>', unsafe_allow_html=True)


# ── Incremental Multi-Step Execution Logic ───────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic in the sidebar.")
    else:
        st.session_state.results = {}
        st.session_state.current_step = "search"
        st.rerun()

if st.session_state.current_step == "search":
    topic_val = st.session_state.topic_input
    search_agent = build_search_agent()
    sr = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
    })
    st.session_state.results["search"] = sr["messages"][-1].content
    st.session_state.current_step = "reader"
    st.rerun()

elif st.session_state.current_step == "reader":
    topic_val = st.session_state.topic_input
    reader_agent = build_reader_agent()
    rr = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic_val}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{st.session_state.results['search'][:800]}"
        )]
    })
    st.session_state.results["reader"] = rr["messages"][-1].content
    st.session_state.current_step = "writer"
    st.rerun()

elif st.session_state.current_step == "writer":
    topic_val = st.session_state.topic_input
    research_combined = (
        f"SEARCH RESULTS:\n{st.session_state.results['search']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{st.session_state.results['reader']}"
    )
    st.session_state.results["writer"] = writer_chain.invoke({
        "topic": topic_val,
        "research": research_combined
    })
    st.session_state.current_step = "critic"
    st.rerun()

elif st.session_state.current_step == "critic":
    st.session_state.results["critic"] = critic_chain.invoke({
        "report": st.session_state.results["writer"]
    })
    st.session_state.current_step = "completed"
    st.rerun()


# ── Main Workspace Canvas ────────────────────────────────────────────────────
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-box"><div class="metric-val">4 Agents</div><div class="metric-lbl">Pipeline Architecture</div></div>', unsafe_allow_html=True)
with m2:
    status_text = "Idle"
    if is_processing:
        status_text = "Processing"
    elif st.session_state.current_step == "completed":
        status_text = "Completed"
    st.markdown(f'<div class="metric-box"><div class="metric-val">{status_text}</div><div class="metric-lbl">System Status</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{len(st.session_state.results)} / 4</div><div class="metric-lbl">Steps Completed</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

r = st.session_state.results

if r:
    st.markdown(f"""
    <div class="canvas-header">
        <div>
            <div class="canvas-title">Document Workspace</div>
            <div style="font-size:0.85rem; font-weight:600; color:#334155;">Target: {st.session_state.topic_input}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    view_tab1, view_tab2, view_tab3 = st.tabs(["📝 Final Research Document", "🧐 Evaluation & Feedback", "🔍 Source Data Logs"])

    with view_tab1:
        with st.container():
            if "writer" in r:
                st.markdown(r["writer"])
                st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
                st.download_button(
                    label="Export Document (.md)",
                    data=r["writer"],
                    file_name=f"research_report_{int(time.time())}.md",
                    mime="text/markdown",
                )
            else:
                st.info("Drafting report... Please wait for step 3.")

    with view_tab2:
        with st.container():
            if "critic" in r:
                st.markdown("### Agent Feedback & Review")
                st.markdown(r["critic"])
            else:
                st.info("Awaiting critic evaluation... Please wait for step 4.")

    with view_tab3:
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                if "search" in r:
                    st.markdown("##### Search Agent Findings")
                    st.info(r["search"])
            with c2:
                if "reader" in r:
                    st.markdown("##### Reader Agent Content")
                    st.success(r["reader"])

else:
    with st.container():
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding: 3rem 1rem;">
            <div style="font-size:2.5rem; margin-bottom:1rem;">🎨</div>
            <div style="font-family:'Outfit', sans-serif; font-size:1.2rem; font-weight:700; color:#000000;">Workspace Ready</div>
            <div style="font-size:0.9rem; font-weight:500; color:#334155; max-width:380px; margin-top:0.25rem;">Enter a topic in the sidebar control panel and click 'Start Pipeline' to begin execution.</div>
        </div>
        """, unsafe_allow_html=True)