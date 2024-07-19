from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class SponsorPerformType(str, Enum):
    new = 'new'
    pending = 'pending'
    approved = 'approved'
    cancelled = 'cancelled'


class SponsorType(str, Enum):
    natural_person = 'natural_person'
    legal_entity = 'legal_entity'


class SponsorBase(BaseModel):
    full_name: str
    phone: str
    amount: float
    organization: Optional[str] = None
    sponsor_perform_type: SponsorPerformType
    sponsor_type: SponsorType


class SponsorCreate(SponsorBase):
    pass


class SponsorUpdate(SponsorBase):
    pass


class Sponsor(SponsorBase):
    id: int

    class Config:
        orm_mode = True
