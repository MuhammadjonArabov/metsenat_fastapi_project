from typing import Optional, List

from pydantic import BaseModel

from app.schemas.sponsor import SponsorCreate, SponsorUpdate
from app.schemas.student import StudentCreate, StudentUpdate


class UniversityBase(BaseModel):
    title: str


class UniversityCreate(UniversityBase):
    pass


class University(UniversityBase):
    id: int

    class Config:
        orm_mode = True


class StudentSponsorBase(BaseModel):
    amount: float
    student: Optional[List[StudentCreate]]
    sponsor: Optional[List[SponsorCreate]]


class StudentSponsorCreate(BaseModel):
    amount: float
    student: Optional[List[StudentCreate]] = None
    sponsor: Optional[List[SponsorCreate]] = None


class StudentSponsorUpdate(StudentSponsorBase):
    student: StudentUpdate
    sponsor: SponsorUpdate


class StudentSponsor(StudentSponsorBase):
    id: int
    student_id: int
    sponsor_id: int

    class Config:
        orm_mode = True
