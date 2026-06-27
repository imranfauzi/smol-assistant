import uuid

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware

from core.llm import instance_llm
from core.prompt import load_prompt

from schemas.agent_schema import AgentInput


# 1. Build the agent
def build_assistant_agent():
    llm = instance_llm()
    assistant_prompt = load_prompt("assistant_prompt")

    tools = []


    return create_agent(      
        model=llm,
        tools=tools,
        system_prompt=assistant_prompt,
        middleware=[
            ModelRetryMiddleware(max_retries=3),
            ToolRetryMiddleware(max_retries=2),
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "ask_user": {
                        "allowed_decisions": ["respond"],
                        "description": "Ask the user for missing information",
                    },
                },
                description_prefix="User input required",
            ),
        ],
    )

def run_assistant_agent(payload: AgentInput):

    user_id = payload.user_id
    session_id = payload.session_id
    user_request = payload.user_request

    assistant_config = {
        "configurable": {
            "thread_id": session_id,
            "checkpoint_ns": user_id,
        }
    }

    assistant_agent = build_assistant_agent()

    result = assistant_agent.invoke(
        {"messages": [{"role": "user", "content": user_request}]},
        config=assistant_config,
    )
    return result["messages"][-1].content
