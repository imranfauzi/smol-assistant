from types import SimpleNamespace

from agents import assistant
from schemas.agent_schema import AgentInput


def test_run_assistant_agent(monkeypatch):
    calls = []

    # Use a fake agent so this test does not call the real LLM.
    class FakeAgent:
        def invoke(self, messages, config, context):
            calls.append((messages, config, context))
            fake_message = SimpleNamespace(content="Hello!")
            return {"messages": [fake_message]}

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
