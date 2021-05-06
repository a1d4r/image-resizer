from pydantic import BaseModel

from app.models import Status


class ResponseTaskID(BaseModel):
    id: str


class ResponseTaskStatus(ResponseTaskID):
    status: Status

    class Config:
        use_enum_values = True
