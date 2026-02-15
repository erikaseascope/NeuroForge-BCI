from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# LLM injected later

# Prompt for Biocompatibility & Safety Validation Agent
BIOCOMPATIBILITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Biocompatibility & Chronic Stability Agent in NeuroForge.
Your role: Evaluate and optimize materials, coatings, electrode geometry, and long-term tissue response for BCI implants.
Focus on: chronic inflammation, gliosis, signal degradation over months/years, encapsulation, immune response modeling,
ISO 10993-6 implantation effects (local tissue response), chronic toxicity projections.

Core constraints:
- All analysis synthetic/hypothetical — no real implant data.
- Flag HIGH RISK if projected chronic degradation >20% at 6 months or immune score <0.85.
- Require HITL if proposing novel material/coating without strong literature precedent.
- Output format: JSON with keys: proposal_summary, material_suggestions, projected_metrics (degradation_pct, stability_score), risks, hitl_required

Current goal: {goal}
Previous design: {current_design}
Safety flags: {safety_flags}
"""),
    ("human", "Propose next iteration for improved chronic biocompatibility."),
])

def create_biocompatibility_agent(llm):
    chain = (
        {
            "goal": RunnablePassthrough(),
            "current_design": lambda x: x.get("current_design", {}),
            "safety_flags": lambda x: x.get("safety_flags", []),
        }
        | BIOCOMPATIBILITY_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain

# Standalone test
if __name__ == "__main__":
    print("Biocompatibility Agent placeholder ready.")
