from aiogram import Router


def get_handlers_router() -> Router:
    from . import start
    from . import upload_cv_handler
    from . import interview_handler
    from . import answer_handler

    router = Router()
    router.include_router(start.router)
    router.include_router(upload_cv_handler.router)
    router.include_router(interview_handler.router)
    router.include_router(answer_handler.router)

    return router
