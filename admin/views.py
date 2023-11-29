from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.db_helper import db_helper
from .crud import get_users, get_user, get_cases, get_case

router = APIRouter(prefix="/admin", tags=["admin"])



templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def main(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None):
    return "Не все так просто, как кажется"


@router.get("/users", response_class=HTMLResponse)
async def users(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None):
    users = await get_users(session)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})


@router.get("/users/{user_id}", response_class=HTMLResponse)
async def user_detail(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None, user_id: int = None):
    if user_id:
        user = await get_user(session, user_id)
        return templates.TemplateResponse(
            "user.html", 
            {
                "request": request, 
                "user": user[0],
                "cases_a": user[1],
                "reason_f": user[2],
                "reason_r": user[3]
                }
            )

@router.get("/cases", response_class=HTMLResponse)
async def cases(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None):
    cases = await get_cases(session)
    return templates.TemplateResponse("case_list.html", {"request": request, "cases": cases})


@router.get("/cases/{case_id}", response_class=HTMLResponse)
async def case_detail(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None, case_id: int = None):
    if case_id:
        case = await get_case(session, case_id)
        return templates.TemplateResponse(
            "case.html", 
            {
                "request": request, 
                "case": case,
                }
            )