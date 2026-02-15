# NeuroForge

**Recursive AI Swarm for Safe BCI Engineering**

The first open-source autonomous engineering framework that designs, simulates, validates, iterates, and certifies brain-computer interfaces — with unbreakable human oversight and zero tolerance for real biological data.

## ✨ Core Features
- 7 specialized BCI agent clusters (Neuralink-inspired)
- Full recursive iteration loops with LangGraph
- Mandatory HITL (Human-in-the-Loop) gates on every high-risk action
- Private encrypted shards — never touches raw neural data
- Blockchain-anchored audit trails
- Synthetic-only simulation engine (Brian2 + NEURON + PyBullet)
- Beautiful Streamlit dashboard + real-time metrics
- Built-in FDA/EU MDR regulatory export templates

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/YOURUSERNAME/neuroforge.git
cd neuroforge

# 2. Install
uv sync          # recommended (or pip install -e .)
cp .env.example .env

# 3. Run the dashboard
streamlit run src/neuroforge/ui/dashboard.py
