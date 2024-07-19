from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from app.models.base import BaseModel


class StudentType(PyEnum):
    BACHELOR = 'bachelor'
    MASTER = 'master'


class SponsorPerformType(PyEnum):
    NEW = 'new'
    PENDING = 'pending'
    APPROVED = 'approved'
    CANCELLED = 'cancelled'


class SponsorType(PyEnum):
    NATURAL_PERSON = 'natural_person'
    LEGAL_ENTITY = 'legal_entity'


class University(BaseModel):
    __tablename__ = 'universities'

    title = Column(String, nullable=False)
    students = relationship("Student", back_populates="university")


class Student(BaseModel):
    __tablename__ = 'students'

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    contract_amount = Column(Integer, nullable=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=True)
    student_type = Column(ChoiceType(StudentType), default=StudentType.MASTER, nullable=True)

    university = relationship("University", back_populates="students")
    student_sponsors = relationship("StudentSponsor", back_populates="student")


class Sponsor(BaseModel):
    __tablename__ = 'sponsor'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String(14), nullable=False)
    amount = Column(Integer, nullable=False)
    organization = Column(String(225), nullable=True)
    sponsor_perform_type = Column(ChoiceType(SponsorPerformType), default=SponsorPerformType.NEW, nullable=True)
    sponsor_type = Column(ChoiceType(SponsorType), default=SponsorType.LEGAL_ENTITY, nullable=True)

    student_sponsors = relationship("StudentSponsor", back_populates="sponsor")


class StudentSponsor(BaseModel):
    __tablename__ = 'student_sponsor'

    amount = Column(Numeric(precision=60, scale=6), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    sponsor_id = Column(Integer, ForeignKey('sponsor.id'))

    student = relationship("Student", back_populates="student_sponsors")
    sponsor = relationship("Sponsor", back_populates="student_sponsors")
