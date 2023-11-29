import uuid
from enum import Enum
from sqlalchemy import Column, Uuid, Time


class Gender(Enum):
    NONE = 'N'
    MALE = 'M'
    FEMALE = 'F'

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=True)
    updated_at = Column(Time, nullable=True)
