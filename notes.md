run docker
docker compose -f docker/docker-compose.yml up

run project
uvicorn src.main:app --reload

initialize alembic
alembic init alembic
