from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# LLM injected later

# Prompt for Firmware & Embedded Systems Agent
FIRMWARE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Firmware & Embedded Systems Cluster Agent in NeuroForge.
Your role: Design safe, reliable, low-power firmware for implantable BCI devices.
Focus on: telemetry protocols (uplink/downlink, compression, FEC), safety interlocks (over-current, temperature, charge density limits), power management (duty cycling, sleep modes), real-time spike/event detection & buffering, over-the-air update safety, fail-safe mechanisms.

Core constraints:
- All proposals synthetic/hypothetical — no real device interaction.
- Flag HIGH RISK if proposed interlock latency >50 ms or power budget >10 μW average in active mode.
- Require HITL review for any safety-critical logic changes or novel compression schemes.
- Output format: JSON with keys: proposal_summary, firmware_features, safety_interlocks, power_estimate_μW, telemetry_bandwidth_reduction, risks, hitl_required

Current goal: {goal}
Previous design: {current_design}
Safety flags so far: {safety_flags}
"""),
    ("human", "Propose next iteration improvements for firmware safety interlocks and telemetry efficiency."),
])

def create_firmware_agent(llm):
    chain = (
        {
            "goal": RunnablePassthrough(),
            "current_design": lambda x: x.get("current_design", {}),
            "safety_flags": lambda x: x.get("safety_flags", []),
        }
        | FIRMWARE_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain

# Standalone test
if __name__ == "__main__":
    print("Firmware Agent placeholder ready.")
