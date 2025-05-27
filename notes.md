!!!activate venv
source venv/Scripts/activate

run docker
docker compose -f docker/docker-compose.yml up

run project
uvicorn app.main:app --reload

run telegram-bot
python -m telegram

run tunnel ngrok (in PowerShell)
.\ngrok.exe http 8000

initialize alembic
(register all models in db/models/__init__)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

run celery (locally, not in container)
celery -A src.celery.celery_app worker --loglevel=info --pool=solo


Як підв'язати форму реєстрації до телеграм (MiniApps)
- create bot in BotFather, get TOKEN
- create folder telegram with bot(setup as in example)
- create folder httpx_clients(here are wrappers of routers for
connection frontend(e.g.Telegram) with backend) - with settings 
  for client(tg connet to backend)
- I added router for webapp in app folder(щоб прокинути 
зміні з дотенв до фронта - html, js)
- create folder webapp - here are html (тут моя форма реєстрації),
script (керує поведінкою форми) and css (for later beauty)
- install ngrok for tunnel between outer app - tg and localhost
- run ngrok, uvicorn. Your form must be available on link:
<https://c67b-195-12-57-124.ngrok-free.app>(forwarding link)/webapp
- if all previous ok - setup tg-menu button in inline keyboard
and handler for it in handlers
- ToDO: add login (when user registered in other way want to work with telegram)