from pydantic import BaseModel
from app.models.student_sponsor import StudentType, SponsorPerformType, SponsorType


class StudentCreate(BaseModel):
    full_name: str
    phone: str
    contract_amount: int
    student_type: StudentType
    university_id: int


class SponsorCreate(BaseModel):
    full_name: str
    phone: str
    amount: int
    organization: str
    sponsor_perform_type: SponsorPerformType
    sponsor_type: SponsorType


class StudentSponsorCreate(BaseModel):
    student: StudentCreate
    sponsor: SponsorCreate
    amount: int


class StudentSponsorAdd(BaseModel):
    student_id: int
    sponsor_id: int
    amount: int

    class Config:
        orm_mode = True
