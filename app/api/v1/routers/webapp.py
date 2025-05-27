# app/routes/webapp.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from httpx_clients.interview_client.config import get_interview_settings

router = APIRouter(tags=["WebApp"], prefix="/webapp")
templates = Jinja2Templates(directory="app")

@router.get("", response_class=HTMLResponse)
async def serve_webapp(request: Request):
    settings = get_interview_settings()
    return templates.TemplateResponse("templates/index.html", {
        "request": request,
        "INTERVIEW_BASE_URL": settings.BASE_URL,
    })
