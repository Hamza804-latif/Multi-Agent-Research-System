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