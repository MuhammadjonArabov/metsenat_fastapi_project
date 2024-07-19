from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import student_sponsor as models
from app.schemas import sponsor
from app.schemas.sponsor import SponsorUpdate
from app.schemas import ss_schemas


async def get_sponsor(db: AsyncSession, sponsor_id: int):
    result = await db.execute(select(models.Sponsor).filter(models.Sponsor.id == sponsor_id))
    return result.scalar_one_or_none()


async def get_sponsor_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Sponsor).offset(skip).limit(limit))
    return result.scalars().all()


async def create_sponsor(
        db: AsyncSession,
        sponsor: ss_schemas.SponsorCreate
):
    sponsor_perform_types = [
        'new', 'pending',
        'approved', 'cancelled'
    ]
    sponsor_types = [
        'natural_person', 'legal_entity'
    ]
    if sponsor.sponsor_perform_type not in sponsor_perform_types:
        raise HTTPException(status_code=400, detail="Noto'g'ri sponsor amal boshlang'ich holati")
    if sponsor.sponsor_type not in sponsor_types:
        raise HTTPException(status_code=400, detail="Noto'g'ri sponsor turi")
    db_sponsor = models.Sponsor(
        full_name=sponsor.full_name,
        phone=sponsor.phone,
        amount=sponsor.amount,
        organization=sponsor.organization,
        sponsor_perform_type=sponsor.sponsor_perform_type,
        sponsor_type=sponsor.sponsor_type,
    )
    db.add(db_sponsor)
    await db.commit()
    await db.refresh(db_sponsor)
    return db_sponsor.id


async def update_sponsor(db: AsyncSession, sponsor_id: int, sponsor: SponsorUpdate):
    db_sponsor = await get_sponsor(db=db, sponsor_id=sponsor_id)
    if db_sponsor:
        db_sponsor.full_name = sponsor.full_name
        db_sponsor.phone = sponsor.phone
        db_sponsor.amount = sponsor.amount
        db_sponsor.sponsor_perform_type = sponsor.sponsor_perform_type
        db_sponsor.sponsor_type = sponsor.sponsor_type
        await db.commit()
        await db.refresh(db_sponsor)
    return db_sponsor


async def search_sponsors(
        db: AsyncSession,
        full_name: str = None,
        phone: str = None,
        organization: str = None,
):
    query = select(models.Sponsor)
    if full_name:
        query = query.where(models.Sponsor.full_name.ilike(f"%{full_name}%"))
    if phone:
        query = query.where(models.Sponsor.phone == phone)
    if organization:
        query = query.where(models.Sponsor.organization.ilike(f"%{organization}%"))
    result = await db.execute(query)
    return result.scalars().all()
