from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models import NewCase, NewPeopleMembers, MemberReason 

async def get_users(session: AsyncSession):
    result = await session.execute(select(NewPeopleMembers))
    return result.scalars().all()

async def get_user(session: AsyncSession, user_id: int)  :
    result = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == user_id))

    cases_a = await session.execute(select(NewCase).where(NewCase.people_accepted.any(NewPeopleMembers.user_id == user_id)))
    cases_f = await session.execute(select(NewCase).where(NewCase.people_fifty.any(NewPeopleMembers.user_id == user_id)))
    cases_r = await session.execute(select(NewCase).where(NewCase.people_rejected.any(NewPeopleMembers.user_id == user_id)))

    reason_f = [{i: [case, (await session.execute(select(MemberReason).where(MemberReason.user_id == user_id, MemberReason.case_id == case.case_id))).scalar()]} for i, case in enumerate(cases_f.scalars().all())]
    reason_r = [{i: [case, (await session.execute(select(MemberReason).where(MemberReason.user_id == user_id, MemberReason.case_id == case.case_id))).scalar()]} for i, case in enumerate(cases_r.scalars().all())]
    return result.scalar(), cases_a.scalars().all(), reason_f, reason_r  

async def get_cases(session: AsyncSession):
    result = await session.execute(select(NewCase))
    return result.scalars().all()

async def get_case(session: AsyncSession, case_id: int):
    statement = select(NewCase).where(NewCase.case_id == case_id).options(selectinload(NewCase.people_accepted), selectinload(NewCase.people_fifty), selectinload(NewCase.people_rejected)) 
    case = await session.execute(statement)
    case = case.scalar()
    return case