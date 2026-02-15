"""
Grokpedia - abstracted knowledge bank (RAG placeholder with Grok LLM integration)
Namespaces: Neural-Signal-Processing, Chronic-Stability, etc.
Uses Grok API via langchain_xai as fallback/query enhancer.
"""

from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env for XAI_API_KEY

# Optional Grok LLM integration (requires langchain-xai installed)
try:
    from langchain_xai import ChatXAI
    GROK_AVAILABLE = True
except ImportError:
    GROK_AVAILABLE = False

class Grokpedia:
    """Simple in-memory store + Grok-powered query fallback"""

    namespaces: Dict[str, List[Dict]] = {
        "Neural-Signal-Processing-Heuristics": [],
        "Chronic-Implant-Stability-Benchmarks": [],
        "Decoding-Model-Adaptation-Strategies": [],
        "Surgical-Robotics-Kinematics": [],
        # Add more as needed from original spec
    }

    @classmethod
    def propose_patch(cls, namespace: str, patch: Dict):
        """Agent proposes update → future guardian/HITL review"""
        if namespace in cls.namespaces:
            cls.namespaces[namespace].append(patch)
            print(f"[Grokpedia] Patch proposed to {namespace}: {patch.get('summary', 'no summary')}")
        else:
            print(f"[Grokpedia] Unknown namespace: {namespace}")

    @classmethod
    def query(cls, namespace: str, query_str: str) -> str:
        """Retrieve from local store or fallback to Grok LLM query if API key present"""
        if namespace in cls.namespaces and cls.namespaces[namespace]:
            # Simple local retrieval (expand to vector search later)
            relevant = [p for p in cls.namespaces[namespace] if query_str.lower() in str(p).lower()]
            if relevant:
                return f"Local Grokpedia hit in {namespace}: {relevant[0]}"

        # Fallback to Grok LLM if available
        api_key = os.getenv("XAI_API_KEY")
        if GROK_AVAILABLE and api_key:
            try:
                llm = ChatXAI(
                    model="grok-4",  # or "grok-beta", "grok-4.1-fast" etc. – adjust as needed
                    xai_api_key=api_key,
                    temperature=0.3,
                )
                response = llm.invoke(
                    f"Provide synthetic, hypothetical knowledge on BCI topic in namespace '{namespace}': {query_str}. "
                    "Keep it abstract, public-domain safe, no real patient data."
                )
                return f"Grok fallback response: {response.content.strip()}"
            except Exception as e:
                return f"Grok query failed: {str(e)} (check XAI_API_KEY or langchain-xai install)"
        
        return f"No local data in {namespace} and Grok fallback not available. Add XAI_API_KEY to .env or install langchain-xai."
