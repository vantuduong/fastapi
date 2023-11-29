from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database import get_db_context
from schemas.base_entity import BaseEntity


def not_found_exception():
    return HTTPException(status_code=404, detail="Item not found")

class BaseService:
    def __init__(self, db: Session = Depends(get_db_context)):
        self._db = db

    def save(self, entity: BaseEntity):
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)

        return entity

    def delete(self, entity: BaseEntity):
        self._db.delete(entity)
        self._db.commit()
