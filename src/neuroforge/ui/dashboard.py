import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

st.set_page_config(
    page_title="NeuroForge Dashboard",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NeuroForge – Safe BCI Engineering Swarm")
st.markdown("Recursive AI agents designing next-generation brain-computer interfaces — with mandatory human oversight.")

st.header("Current Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Iteration", "0 / —")
    st.metric("Human Touch Hours", "< 0.1 h")

with col2:
    st.metric("Safety Flags", "0 active")
    st.metric("Requires HITL", "No")

with col3:
    st.metric("Best Metric", "— bits/s")
    st.metric("Chronic Stability Proj.", "— %")

st.subheader("Goal / Prompt")
goal = st.text_area(
    "Enter design goal (example: 'Optimize 1024-channel array for <15% signal loss at 12 months')",
    height=100,
    value="Reduce chronic signal degradation by 30% in simulated 6-month implant"
)

if st.button("Start Swarm Iteration", type="primary"):
    st.info("Swarm starting... (agents not yet connected in v0.1)")
    st.warning("This is a placeholder — real recursion coming in next updates.")

st.subheader("Audit Trail (last entries)")
st.text("2026-02-15 14:30 – Iteration 0 initialized – HITL gate passed")

st.sidebar.title("Controls")
st.sidebar.button("Emergency Stop")
st.sidebar.checkbox("Enable verbose logging", value=True)
st.sidebar.selectbox("LLM Backend", ["Grok", "Local Llama", "Claude"], index=0)
