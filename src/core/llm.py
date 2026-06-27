
from core.config import settings
from langchain_openai import ChatOpenAI

def instance_llm():
    try:
        llm = ChatOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_MODEL
        )
        return llm
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        raise RuntimeError("Failed to initialize LLM") from e
