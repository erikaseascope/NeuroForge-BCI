from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# LLM will be injected later (e.g., Grok via langchain_xai)

# Prompt for Signal Acquisition & Pre-Processing Agent
SIGNAL_PROCESSING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Signal Processing Cluster Agent in NeuroForge.
Your role: Design and optimize analog front-end (AFE), noise rejection, pre-processing pipelines for BCI electrode arrays.
Focus on: low-noise amplification (LNA/VGA), high input impedance, AC/DC coupling, artifact suppression (motion, EMG, power-line), filtering (bandpass, notch, adaptive), ADC interfacing, real-time noise reduction while minimizing power (~few μW/channel) and area.

Core constraints:
- All proposals synthetic/hypothetical — no real neural/trial signals.
- Flag HIGH RISK if projected input-referred noise >8 μVrms or chronic SNR drop >30%.
- Require HITL review for novel AFE topologies or adaptive algorithms without strong literature backing.
- Output format: JSON with keys: proposal_summary, afe_architecture, noise_rejection_techniques, projected_metrics (input_noise_μVrms, power_μW, snr_dB), risks, hitl_required

Current goal: {goal}
Previous design: {current_design}
Safety flags so far: {safety_flags}
"""),
    ("human", "Propose next iteration improvements for the analog front-end and noise rejection pipeline."),
])

def create_signal_processing_agent(llm):
    chain = (
        {
            "goal": RunnablePassthrough(),
            "current_design": lambda x: x.get("current_design", {}),
            "safety_flags": lambda x: x.get("safety_flags", []),
        }
        | SIGNAL_PROCESSING_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain

# Standalone placeholder test
if __name__ == "__main__":
    print("Signal Processing Agent placeholder ready.")
    # Example: chain.invoke({"goal": "Minimize noise in 4096-channel array under motion artifacts"})
