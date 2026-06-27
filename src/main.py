

from core.config import settings

def main():
    print(f"llm model: {settings.LLM_API_KEY}")



if __name__=="__main__":
    main()