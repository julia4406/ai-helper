import asyncio
import fitz     # PyMuPDF

from typing import Optional
from fastapi import UploadFile
from loguru import logger


async def extract_text_from_pdf(upload_file: UploadFile) -> Optional[str]:
    contents = await upload_file.read()

    # TODO: Can be improved (async context)
    def extract_text() -> str:
        logger.debug("Start reading PDF content")
        with fitz.open(stream=contents, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc).strip()

    try:
        return await asyncio.to_thread(extract_text)
    except Exception as e:
        print(f"Failed to read PDF: {e}")
        return None
