import subprocess

subprocess.run(["uvicorn", "src.main:app", "--port", "8000", "--reload"])
