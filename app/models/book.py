from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import Field, BaseModel, ValidationError, field_validator
from fastapi import HTTPException

from database import get_db_context, SessionLocal
from models.author import AuthorViewModel
from models.user import UserViewModel
from schemas.author import Author


class BookFormModel(BaseModel):
    title: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    author_id: UUID
    is_published: bool = Field(default=False)

    @field_validator('author_id')
    @classmethod
    def check_author_exist(cls, value):
        db = SessionLocal()
        try:
            author = db.query(Author).filter(Author.id == value).first()
            if not author:
                raise HTTPException(status_code=422, detail='Author id is not correct')
            return value
        finally:
            db.close()



class BookListModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    rating: int
    author_id: UUID
    is_published: bool = True

class BookDetailModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    rating: int
    author_id: UUID
    author: AuthorViewModel
    user_id: UUID | None = None
    owner: UserViewModel | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
