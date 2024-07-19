from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

from app.schemas.sponsor import Sponsor


class StudentType(str, Enum):
    bachelor = 'bachelor'
    master = 'master'


class StudentCreate(BaseModel):
    full_name: Optional[str] = None
    phone: str
    contract_amount: Optional[float] = None
    student_type: Optional[StudentType] = None
    university_id: Optional[int] = None
