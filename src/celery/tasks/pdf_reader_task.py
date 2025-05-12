import fitz
from celery import shared_task

from loguru import logger


# TODO remade into task (all services inside compose)
@shared_task
def read_from_pdf(upload_file: bytes) -> str | None:
    pass
