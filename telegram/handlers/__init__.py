from aiogram import Router


def get_handlers_router() -> Router:
    from . import start
    from . import upload_cv
    from . import interview

    router = Router()
    router.include_router(start.router)
    router.include_router(upload_cv.router)
    router.include_router(interview.router)

    return router
