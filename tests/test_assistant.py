import os
from pathlib import Path
from types import SimpleNamespace


PROJECT_ROOT = Path(__file__).resolve().parents[1]

os.environ.setdefault("LLM_BASE_URL", "https://example.test")
os.environ.setdefault("LLM_API_KEY", "test-key")
os.environ.setdefault("LLM_MODEL", "test-model")
os.environ.setdefault("MLFLOW_TRACKING_URI", "file:///tmp/mlflow")
os.environ.setdefault("MLFLOW_EXPERIMENT_NAME", "test")
os.environ.setdefault("WORKING_PATH", "/tmp")
os.environ.setdefault("CHECKPOINTER_PATH", "/tmp/checkpointer.sqlite")
os.environ.setdefault("CHROMADB_PATH", "/tmp/chromadb")
os.environ.setdefault("RAW_DOCS_PATH", "/tmp/raw-docs")
os.environ.setdefault("HUEY_QUEUE_PATH", "/tmp/huey.sqlite")
os.environ.setdefault("PROMPT_PATH", str(PROJECT_ROOT / "prompts"))

from agents import assistant
from schemas.agent_schema import AgentInput


def test_run_assistant_agent(monkeypatch):
    calls = []

    class FakeAgent:
        def invoke(self, messages, config, context):
            calls.append((messages, config, context))
            return {"messages": [SimpleNamespace(content="Hello!")]}

    monkeypatch.setattr(assistant, "build_assistant_agent", lambda: FakeAgent())

    payload = AgentInput(
        user_request="Hi",
        session_id="session-1",
        user_id="user-1",
    )

    result = assistant.run_assistant_agent(payload)

    assert result == "Hello!"
    assert calls[0][0] == {"messages": [{"role": "user", "content": "Hi"}]}
    assert calls[0][1]["configurable"]["thread_id"] == "session-1"
    assert calls[0][1]["configurable"]["checkpoint_ns"] == "user-1"
    assert calls[0][2].thread_id == "session-1"
    assert calls[0][2].user_id == "user-1"
