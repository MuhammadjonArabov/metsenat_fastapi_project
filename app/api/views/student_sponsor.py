from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.sponsor import update_sponsor, get_sponsor, get_sponsor_list, create_sponsor
from app.crud.student import create_student, create_university, get_student_list
from app.crud.student_sponsor import create_student_sponsor
from app.schemas import sponsor, student, student_sponsor
from app.schemas import ss_schemas
from app.models.student_sponsor import StudentSponsor, Student, Sponsor
from sqlalchemy.future import select
from app.schemas.new_student import StudentRead, StudentCreate as StudentCreates

router = APIRouter()


@router.get("/students/{student_id}", response_model=StudentRead)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return {"detail": "Student deleted"}


@router.put("/students/{student_id}", response_model=StudentRead)
async def update_student(student_id: int, updated_data: StudentCreates, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.full_name = updated_data.full_name
    student.phone = updated_data.phone
    student.contract_amount = updated_data.contract_amount
    student.university_id = updated_data.university_id
    student.student_type = updated_data.student_type
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/student/")
async def read_student(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    sponsors = await get_student_list(db=db, skip=skip, limit=limit)
    return sponsors


@router.post("/university/")
async def create_universityes(university: student_sponsor.UniversityCreate, db: AsyncSession = Depends(get_db)):
    return await create_university(db=db, university=university)


@router.post("/sponsors/")
async def create_sponsors(sponsor: sponsor.SponsorCreate, db: AsyncSession = Depends(get_db)):
    return await create_sponsor(db=db, sponsor=sponsor)


@router.get("/sponsors/")
async def read_sponsors(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    sponsors = await get_sponsor_list(db=db, skip=skip, limit=limit)
    return sponsors


@router.get("/sponsors/{sponsor_id}")
async def read_sponsor(sponsor_id: int, db: AsyncSession = Depends(get_db)):
    db_sponsor = await get_sponsor(db=db, sponsor_id=sponsor_id)
    if db_sponsor is None:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return db_sponsor


@router.put("/sponsors/{sponsor_id}")
async def update_sponsors(sponsor_id: int, sponsor: sponsor.SponsorUpdate, db: AsyncSession = Depends(get_db)):
    db_sponsor = await update_sponsor(db=db, sponsor_id=sponsor_id, sponsor=sponsor)
    if db_sponsor is None:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return db_sponsor


@router.post("/students/")
async def create_students(student: student.StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = await create_student(db=db, student=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student could not be created")
    return db_student


@router.post("/student_sponsors/")
async def create_student_sponsors(
        student_sponsor: ss_schemas.StudentSponsorCreate,
        db: AsyncSession = Depends(get_db)

):
    return await create_student_sponsor(db=db, student_sponsor=student_sponsor)


@router.post(
    "/add_student_sponsor/",
)
async def add_sponsor(
        data: ss_schemas.StudentSponsorAdd,
        db: AsyncSession = Depends(get_db),
):
    result = StudentSponsor(
        amount=data.amount,

    )
    db.add(result)
    await db.flush()
    if data.student_id:
        a = await db.execute(select(Student).where(Student.id == data.student_id))
        stu = a.scalars().first()
        if stu:
            result.student_id = stu.id
        else:
            HTTPException(
                status_code=404,
                detail='stu yoq'
            )
    if data.sponsor_id:
        a = await db.execute(select(Sponsor).where(Sponsor.id == data.sponsor_id))
        spo = a.scalars().first()
        if spo:
            result.sponsor_id = spo.id
        else:
            HTTPException(
                status_code=404,
                detail='spo yoq'
            )
    if data.student_id and data.sponsor_id:
        query = select(Sponsor).join(StudentSponsor).join(Student).where(
            StudentSponsor.amount > Student.contract_amount)
        result = await db.execute(query)
        sponsor = result.scalars().first()
        if sponsor:
            result.sponsor_id = sponsor.id
        else:
            raise HTTPException(status_code=404,
                                detail="StudentSponsorni amounti Studentni contract amountidan katta bo'lmasligi kerak!")
    await db.commit()
    await db.refresh(result)
    return {
        'id': result.id,
        "student_id": result.student_id,
        "sponsor_id": result.sponsor_id,
        "amount": result.amount
    }
