from fastapi import APIRouter

from app.api.v1.routers.healthcheck import router as healthcheck_router
from app.api.v1.routers.user import router as user_router
from app.api.v1.routers.user_profile import router as user_profile_router
from app.api.v1.routers.interview import router as interview_router
from app.api.v1.routers.webapp import router as webapp_router


router = APIRouter()

router.include_router(healthcheck_router)
router.include_router(user_router)
router.include_router(user_profile_router)
router.include_router(interview_router)
router.include_router(webapp_router)
