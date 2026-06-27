from typing import Optional
from pydantic import BaseModel, Field

class AgentInput(BaseModel):
    user_request: str = Field(..., description="The prompt provided by the user.")
    session_id: str = Field(..., description="Session id for current agent run")
    user_id: Optional[str] = Field(None, description="user id for current agent run")
