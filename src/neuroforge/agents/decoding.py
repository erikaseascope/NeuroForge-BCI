from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# We'll add LLM import later when we wire the backend

# Placeholder prompt for the Decoding Agent
DECODING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Decoding Cluster Agent in NeuroForge.
Your role: Design, optimize, and validate spike sorting + intention decoding algorithms for BCI systems.
Focus on: spike detection, sorting accuracy, adaptive Kalman/filter models, bits-per-second throughput,
drift resistance, low-latency real-time decoding.

Core constraints:
- All proposals must be synthetic / simulation-only.
- Flag any design with >5% projected chronic degradation as HIGH RISK.
- Suggest HITL review if decoding accuracy claim > state-of-the-art by >15%.
- Output format: JSON with keys: proposal_summary, key_innovations, projected_metrics, risks, hitl_required

Current iteration goal: {goal}
Previous design: {current_design}
Safety flags so far: {safety_flags}
"""),
    ("human", "Propose next iteration improvements for the decoding pipeline."),
])

# Simple runnable skeleton (LLM will be injected later)
def create_decoding_agent(llm):
    chain = (
        {
            "goal": RunnablePassthrough(),
            "current_design": lambda x: x.get("current_design", {}),
            "safety_flags": lambda x: x.get("safety_flags", []),
        }
        | DECODING_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain

# Example usage (for testing standalone)
if __name__ == "__main__":
    print("Decoding Agent placeholder ready.")
    # In real use: chain.invoke({"goal": "Improve spike sorting for noisy 4096-channel array"})
