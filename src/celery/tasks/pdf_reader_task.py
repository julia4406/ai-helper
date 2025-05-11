import fitz
from celery import shared_task


@shared_task
def extract_text_from_pdf(upload_file: bytes) -> str:
    try:
        with fitz.open(stream=upload_file, filetype="pdf") as doc:
          text = ""
          for page in doc:
              text += page.get_text()
          return text.strip()
    except Exception as e:
      print(f"Failed to read PDF: {e}")
      return None
