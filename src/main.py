import uuid
from agents.assistant import run_assistant_agent

from schemas.agent_schema import AgentInput

def main():

    assistant_payload = AgentInput(
        user_id='user123',
        session_id=str(uuid.uuid4()),
        user_request="Who is Prime minister of malaysia today"
    )
    try:
        result_assistant_agent = run_assistant_agent(assistant_payload)
        print(result_assistant_agent)
    except Exception as e:
        print(f"Assistant failed: {e}")

if __name__=="__main__":
    main()