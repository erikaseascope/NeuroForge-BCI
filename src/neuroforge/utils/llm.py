import os
from langchain_xai import ChatXAI

def get_llm(model="grok-4", temperature=0.3):
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY not set in .env")
    return ChatXAI(
        model=model,
        xai_api_key=api_key,
        temperature=temperature,
    )
