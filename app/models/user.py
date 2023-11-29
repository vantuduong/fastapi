from uuid import UUID

from pydantic import BaseModel

class UserViewModel(BaseModel):
    id: UUID
    username: str
    email: str

    class Config:
        from_attributes = True
