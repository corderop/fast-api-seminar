# Benefit Management System

API for managing benefit plans, enrollments, and claims. A simple FastAPI project managed with [uv](https://docs.astral.sh/uv/).

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
uv sync
```

## Run

```bash
uv run dev
```

The `dev` task is a project script defined in `pyproject.toml` (`app.cli:dev`) that starts uvicorn with auto-reload. Options:

```bash
uv run dev --port 9000
uv run dev --host 0.0.0.0 --port 9000
uv run dev --no-reload
```

Then open:

- http://127.0.0.1:8000/departments — departments endpoint
- http://127.0.0.1:8000/docs — Swagger UI
- http://127.0.0.1:8000/redoc — ReDoc

## Endpoints

| Method | Path            | Description          |
| ------ | --------------- | -------------------- |
| GET    | `/departments`  | Department benefits  |


## Try it

```bash
curl http://127.0.0.1:8000/departments
```

## Layout

```
app/
  main.py             # FastAPI app and routes
  cli.py              # dev entry point (uv run dev)
  schemas.py          # Pydantic models
  routers/benefits.py # Benefits CRUD router (not mounted yet)
```
