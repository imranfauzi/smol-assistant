from typing import Optional
from pydantic import BaseModel, Field

class AgentInput(BaseModel):
    user_request: str = Field(..., description="The prompt provided by the user.")
    session_id: str = Field(..., description="Session id for current agent run")
    user_id: Optional[str] = Field(None, description="user id for current agent run")


class AgentTagsInput(BaseModel):
    thread_id: str = Field(..., description="The unique identifier for the current conversation thread.")
    agent_role: str = Field(..., description="The assigned role or persona of the executing agent.")
    job_id: str | None = Field(default=None, description="Optional tracking identifier for a background batch execution job.")
    task_id: str | None = Field(default=None, description="Optional precise identifier for a sub-step task within a workflow.")