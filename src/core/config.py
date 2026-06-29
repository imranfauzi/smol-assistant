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

    # WORKING DIR
    WORKING_PATH: str

    # AGENT MEMORY
    CHECKPOINTER_PATH: str

    # RAG
    CHROMADB_PATH:str
    RAW_DOCS_PATH: str

    # HUEY
    HUEY_QUEUE_PATH: str

    # PROMPT
    PROMPT_PATH: str

    # TOOL: google_search
    SERPER_URL: str
    SERPER_API_KEY: SecretStr
        

settings = Settings()