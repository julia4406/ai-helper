!!!activate venv
source venv/Scripts/activate

run docker
docker compose -f docker/docker-compose.yml up

run project
uvicorn src.main:app --reload

initialize alembic
(register all models in db/models/__init__)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

run celery (locally, not in container)
celery -A src.celery.celery_app worker --loglevel=info --pool=solo

при спробі підтягнути готове св в інтерв'ю помилка 422