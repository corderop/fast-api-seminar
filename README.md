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

| Method | Path                  | Description                            |
| ------ | --------------------- | -------------------------------------- |
| GET    | `/departments`        | Department benefits                    |
| GET    | `/departments/{id}`   | Single department                      |
| POST   | `/departments`        | Create a department                    |

`GET /departments` accepts an optional `benefit` query parameter to return only
the departments that offer that benefit:

```bash
curl "http://127.0.0.1:8000/departments?benefit=Comida"
```

## Try it

```bash
curl http://127.0.0.1:8000/departments
```

```bash
curl -X POST http://127.0.0.1:8000/departments \
  -H "Content-Type: application/json" \
  -d '{"name": "Tecnología", "benefits": ["Comida", "Transporte"]}'
```

## API client (Bruno)

The [`.bruno/`](.bruno) folder is a [Bruno](https://www.usebruno.com/) collection
covering every endpoint above, including the 404 branch.

1. Start the API with `uv run dev`.
2. In Bruno, choose **Collection → Open Collection** and select the `.bruno/` folder.
   The folder is hidden by default, so press <kbd>⌘</kbd>+<kbd>⇧</kbd>+<kbd>.</kbd>
   in the picker, or press <kbd>⌘</kbd>+<kbd>⇧</kbd>+<kbd>G</kbd> and paste the path.
3. Select the **Local** environment (`baseUrl` = `http://127.0.0.1:8000`).

Requests include tests, so the collection can also run headlessly:

```bash
cd .bruno
npx @usebruno/cli run --env Local
```

The CLI must run from the collection root, so `cd` first.

## Layout

```
app/
  main.py                          # FastAPI app, mounts module routers
  cli.py                           # dev entry point (uv run dev)
  departments/                     # departments module
    utils.py                       # Module helpers (getNextId)
    controllers/departments.py     # HTTP routes, status codes, HTTP errors
    use_cases/                     # One file per use case
      get_departments.py           # List departments (optional benefit filter)
      get_department.py            # Fetch one department
      create_department.py         # Create a department
    repositories/departments.py    # In-memory storage and id generation
```

Each module is a package under `app/` split into three layers:

- `controllers` — FastAPI routers and request/response handling.
- `use_cases` — business rules, independent of HTTP.
- `repositories` — data access and persistence.

Requests flow `controller → use case → repository`; controllers never touch storage directly.
