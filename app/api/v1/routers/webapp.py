import json

import httpx
from aiogram.fsm.context import FSMContext
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from httpx_clients.interview_client.config import get_interview_settings
from telegram.core.config import get_tg_settings

from pydantic import BaseModel

from telegram.core.loader import dp
from telegram.handlers.start_handler import start_message


class StartCommandData(BaseModel):
    chat_id: int
    text: str


class ManualInterviewData(BaseModel):
    job_position: str
    experience: float
    tech_stack: str
    telegram_id: str


router = APIRouter(tags=["WebApp"], prefix="/webapp")
templates = Jinja2Templates(directory="app")

@router.get("", response_class=HTMLResponse)
async def serve_webapp(request: Request):
    settings = get_interview_settings()
    return templates.TemplateResponse("templates/index.html", {
        "request": request,
        "INTERVIEW_BASE_URL": settings.BASE_URL,
    })


@router.get("/interview-form", response_class=HTMLResponse)
async def serve_manual_webapp(request: Request):
    settings = get_interview_settings()
    return templates.TemplateResponse("templates/profile_data.html", {
        "request": request,
        "INTERVIEW_BASE_URL": settings.BASE_URL,
    })


@router.post("/telegram/send_start_command/")
async def send_start_command(data: StartCommandData):
    settings = get_tg_settings()
    telegram_id = str(data.chat_id)

    get_state = dp.get_current()
    state: FSMContext = get_state.fsm.resolve_context(
        chat_id=data.chat_id, user_id=data.chat_id
    )
    text, reply_markup = await start_message(telegram_id, state)


    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{settings.TOKEN}/sendMessage",
            json={
                "chat_id": telegram_id,
                "text": text,
                "reply_markup": reply_markup.model_dump(exclude_none=True)
            }
        )

    return {"status": "ok"}
