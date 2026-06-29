import uuid

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware

from core.llm import instance_llm
from core.prompt import load_prompt
from core.checkpointer import get_assistant_memory

from schemas.context_schema import Context
from schemas.agent_schema import AgentInput

from tools.current_time import get_current_time
from tools.google_search import google_search

# 1. Build the agent
def build_assistant_agent():
    llm = instance_llm()
    assistant_prompt = load_prompt("assistant_prompt")
    assistant_memory = get_assistant_memory()


    tools = [get_current_time, google_search]
    return create_agent(      
        model=llm,
        tools=tools,
        system_prompt=assistant_prompt,
        checkpointer=assistant_memory,
        context_schema=Context,
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
        context=Context(thread_id=session_id, user_id=user_id)
    )
    return result["messages"][-1].content
