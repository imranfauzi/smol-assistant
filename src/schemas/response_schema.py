from typing import Optional
from pydantic import BaseModel


class CustomResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None