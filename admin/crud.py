from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import NewCase, NewPeopleMembers, MemberReason 

async def get_users(session: AsyncSession)  :
    result = await session.execute(select(NewPeopleMembers))
    return result.scalars().all()

async def get_user(session: AsyncSession, user_id: int)  :
    result = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == user_id))
    return result.scalar()