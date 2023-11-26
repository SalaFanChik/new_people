from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.db_helper import db_helper
from .crud import get_users, get_user

router = APIRouter(prefix="/admin", tags=["admin"])

router.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def users(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None):
    users = await get_users(session)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@router.get("/{user_id}", response_class=HTMLResponse)
async def user(session: AsyncSession = Depends(db_helper.session_dependency), request: Request = None, user_id: int = None):
    if user_id:
        user = await get_user(session, user_id)
        return templates.TemplateResponse("user.html", {"request": request, "user": user})