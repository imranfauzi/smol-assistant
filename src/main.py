import uuid

from agents.assistant import run_assistant_agent
from schemas.agent_schema import AgentInput, AgentTagsInput
from core.mlflow import setup_mlflow, set_agent_tags


def main():

    session_id = str(uuid.uuid4())
    user_id = 'user123'
    user_request = "what time is it?"

    # mlflow: init
    setup_mlflow()
    assistant_agent_tags = AgentTagsInput(
        thread_id=session_id,
        agent_role="assistant"
    )
    set_agent_tags(assistant_agent_tags)

    # agent: init
    assistant_payload = AgentInput(
        user_id=user_id,
        session_id=session_id,
        user_request=user_request
    )
    try:
        result_assistant_agent = run_assistant_agent(assistant_payload)
        print(result_assistant_agent)
    except Exception as e:
        print(f"Assistant failed: {e}")

if __name__=="__main__":
    main()