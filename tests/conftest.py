import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# These values let tests import app settings without needing a real .env file.
TEST_ENV = {
    "LLM_BASE_URL": "https://example.test",
    "LLM_API_KEY": "test-key",
    "LLM_MODEL": "test-model",
    "MLFLOW_TRACKING_URI": "file:///tmp/mlflow",
    "MLFLOW_EXPERIMENT_NAME": "test",
    "WORKING_PATH": "/tmp",
    "CHECKPOINTER_PATH": "/tmp/checkpointer.sqlite",
    "CHROMADB_PATH": "/tmp/chromadb",
    "RAW_DOCS_PATH": "/tmp/raw-docs",
    "HUEY_QUEUE_PATH": "/tmp/huey.sqlite",
    "PROMPT_PATH": str(PROJECT_ROOT / "prompts"),
    "SERPER_URL": "https://google.serper.dev/search",
    "SERPER_API_KEY": "test-key",
}

for key, value in TEST_ENV.items():
    os.environ.setdefault(key, value)
