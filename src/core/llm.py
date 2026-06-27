
from core.config import settings
from langchain_openai import ChatOpenAI

from schemas.response_schema import CustomResponse

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
        raise CustomResponse(
            status="error", 
            message="Failed to initialize LLM",
            data={"error": str(e)}
        )
