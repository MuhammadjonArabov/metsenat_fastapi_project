from pydantic import BaseModel
from typing import List, Optional

from app.models.student_sponsor import StudentType


class UniversityCreate(BaseModel):
    title: str


class UniversityRead(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    full_name: str
    phone: str
    contract_amount: Optional[int] = None
    university_id: Optional[int] = None
    student_type: Optional[StudentType] = StudentType.MASTER


class StudentRead(BaseModel):
    id: int
    full_name: str
    phone: str
    contract_amount: Optional[int]
    university_id: Optional[int]
    student_type: StudentType

    class Config:
        orm_mode = True
