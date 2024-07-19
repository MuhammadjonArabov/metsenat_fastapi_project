from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import student, student_sponsor, ss_schemas
from app.models import student_sponsor as models


async def create_student(
        db: AsyncSession,
        student: ss_schemas.StudentCreate
):
    db_student = models.Student(
        full_name=student.full_name,
        phone=student.phone,
        contract_amount=student.contract_amount,
        student_type=student.student_type
    )
    db.add(db_student)
    await db.flush()
    if student.university_id:
        result = await db.execute(select(models.University).where(models.University.id == student.university_id))
        university = result.scalars().first()
        if university:
            db_student.university_id = university.id
        else:
            raise HTTPException(
                status_code=404,
                detail='univer yoq'
            )
    await db.commit()
    await db.refresh(db_student)
    return db_student.id


async def create_university(db: AsyncSession, university: student_sponsor.UniversityCreate):
    db_university = models.University(
        title=university.title
    )
    db.add(db_university)
    await db.commit()
    await db.refresh(db_university)
    return db_university


async def get_student_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Sponsor).offset(skip).limit(limit))
    return result.scalars().all()
