from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding='utf-8', env_ignore_empty=True)

    # LLM 
    LLM_BASE_URL: str
    LLM_API_KEY: SecretStr
    LLM_MODEL: str

    # MLFLOW
    MLFLOW_TRACKING_URI: str
    MLFLOW_EXPERIMENT_NAME: str
    MLFLOW_SUPPRESS_PRINTING_URL_TO_STDOUT: str = "true"
    MLFLOW_LOGGING_LEVEL: str = "ERROR"
    MLFLOW_TRACKING_USERNAME: str
    MLFLOW_TRACKING_PASSWORD: SecretStr
    MLFLOW_WORKSPACE_NAME: str

    # WORKING DIR
    WORKING_PATH: str

    # AGENT MEMORY
    CHECKPOINTER_PATH: str = str(PROJECT_ROOT / "data" / "checkpointer")

    # RAG
    CHROMADB_PATH: str = str(PROJECT_ROOT / "data" / "chromadb")
    RAW_DOCS_PATH: str = str(PROJECT_ROOT / "kb")

    # HUEY
    HUEY_QUEUE_PATH: str = str(PROJECT_ROOT / "data" / "huey")

    # PROMPT
    PROMPT_PATH: str = str(PROJECT_ROOT / "src" / "prompts")

    # TOOL: google_search
    SERPER_URL: str
    SERPER_API_KEY: SecretStr

    # SKILL
    SKILL_PATH: str = str(PROJECT_ROOT / "src" / "skills")
        

settings = Settings()
