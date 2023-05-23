# StrikeBall Passports server

## Before you start the project, you need to take a couple of steps:
- cp .env.example .env
- cp docker-compose.yaml.example docker-compose.yaml

## First start with docker:
- docker-compose build
- docker-compose up database -d (Windows) / docker-compose ub -d database (Linux)
- docker-compose run app alembic upgrade head
- docker-compose up

## The other times
- docker-compose up

# Be careful. PSQL stores its state in the parent folder/data

# Chosen stack

| Framework | DBMS       |
|-----------|------------|
| FastAPI   | PostgreSQL |

# API docs you can see at
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`