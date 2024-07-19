from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.crud.sponsor import create_sponsor
from app.crud.student import create_student
from app.models import student_sponsor as models
from app.schemas.student_sponsor import StudentSponsorCreate, StudentSponsorUpdate
from app.schemas import ss_schemas


async def create_student_sponsor(
        db: AsyncSession,
        student_sponsor: ss_schemas.StudentSponsorCreate,
):

    db_student = await create_student(db=db, student=student_sponsor.student)
    if not db_student:
        raise HTTPException(
            status_code=404,
            detail='student yoq'
        )

    # Create the sponsor
    db_sponsor = await create_sponsor(db=db, sponsor=student_sponsor.sponsor)
    if not db_sponsor:
        raise HTTPException(
            status_code=404,
            detail='sponsor yoq'
        )

    new_student_sponsor = models.StudentSponsor(
        amount=student_sponsor.amount,
        student_id=db_student,
        sponsor_id=db_sponsor

    )

    db.add(new_student_sponsor)
    await db.commit()
    await db.refresh(new_student_sponsor)

    return new_student_sponsor




async def update_student_sponsor(db: AsyncSession, student_sponsor_id: int,
                                 student_sponsor_update: StudentSponsorUpdate):
    db_student_sponsor = db.query(models.StudentSponsor).filter(models.StudentSponsor.id == student_sponsor_id).first()

    if db_student_sponsor:
        for field, value in student_sponsor_update.dict(exclude_unset=True).items():
            setattr(db_student_sponsor, field, value)

        await db.commit()
        await db.refresh(db_student_sponsor)

    return db_student_sponsor


async def get_student_sponsor(db: AsyncSession, student_sponsor_id: int):
    async with db() as session:
        result = await session.execute(
            select(models.StudentSponsor).filter(models.StudentSponsor.id == student_sponsor_id))
        return result.scalars().first()
