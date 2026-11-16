# Benefit Management System

API for managing benefit plans, enrollments, and claims. A simple FastAPI project managed with [uv](https://docs.astral.sh/uv/).

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/) with Compose

## Setup

Start PostgreSQL and install dependencies:

```bash
docker compose up -d db
uv sync
uv run db-init
```

`docker compose up -d db` starts PostgreSQL 17 on `127.0.0.1:5432` and creates
two databases: `bms` for development and `bms_test` for the acceptance suite.
`uv run db-init` creates the schema and the default user.

The application connects with `DATABASE_URL`, which defaults to:

```
postgresql://bms:bms@127.0.0.1:5432/bms
```

Override it for another database:

```bash
export DATABASE_URL="postgresql://user:password@host:5432/database"
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

## Test

Run the unit test suite:

```bash
uv run test-unit
```

Run the acceptance test suite:

```bash
uv run test-acceptance
```

Both tasks are project scripts defined in `pyproject.toml` (`app.cli:test_unit`
and `app.cli:test_acceptance`) that run pytest. Pass a path to run a single
module, or any other pytest option:

```bash
uv run test-unit tests/unit/test_create_department.py
uv run test-unit -k create_department
```

Unit tests live in `tests/unit/` and mock the repositories, so they never touch
PostgreSQL. Acceptance tests live in `tests/acceptance/` and exercise the API
through `TestClient` against the `bms_test` database. Start the database first:

```bash
docker compose up -d db
uv run test-acceptance
```

Acceptance tests create rows with the factories in `app/factories/` and reset
the `bms_test` database between tests. Point them at another database with
`TEST_DATABASE_URL`.

## Seed data

`uv run seed` populates the database with fake departments and users generated
by [Faker](https://faker.readthedocs.io/) and persisted through the factories:

```bash
uv run seed
uv run seed --departments 50 --users 10
uv run seed --clear --random-seed 42
```

| Option           | Default | Description                                      |
| ---------------- | ------- | ------------------------------------------------ |
| `--departments`  | `20`    | Number of departments to create                  |
| `--users`        | `5`     | Number of users to create beyond the default one |
| `--clear`        | off     | Delete existing rows first                       |
| `--random-seed`  | unset   | Seed Faker for reproducible output               |

The default user is created when the schema is initialized.

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

Optionally seed some departments first:

```bash
uv run seed
```

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
  cli.py                           # dev, db-init, seed, and test entry points
  db.py                            # PostgreSQL connections and schema helpers
  schema.sql                       # Tables and indexes (pure SQL, no ORM)
  factories/                       # Faker-backed factories for seed data and tests
    departments.py                 # Department data builder and persistence factory
    users.py                       # User data builder and persistence factory
    fake.py                        # Shared Faker instance
  auth/                            # user persistence
    config.py                      # Environment-driven settings
    passwords.py                   # PBKDF2 hashing and salt generation
    repositories/users.py          # SQL access to the users table
  departments/                     # departments module
    controllers/departments.py     # HTTP routes, status codes, HTTP errors
    use_cases/                     # One file per use case
      get_departments.py           # List departments (optional benefit filter)
      get_department.py            # Fetch one department
      create_department.py         # Create a department
    repositories/departments.py    # SQL access to departments and benefits
tests/
  unit/                            # Use case tests with mocked repositories
  acceptance/                      # API tests against the bms_test database
docker/
  postgres/init.sql                # Creates the bms_test database
compose.yaml                       # PostgreSQL service
```

Each module is a package under `app/` split into three layers:

- `controllers` — FastAPI routers and request/response handling.
- `use_cases` — business rules, independent of HTTP.
- `repositories` — data access and persistence.

Requests flow `controller → use case → repository`; controllers never touch
storage directly. Repositories use [psycopg](https://www.psycopg.org/psycopg3/)
and plain SQL, without an ORM:

- `users` stores one row per user with `salt` and `password_hash`.
- `departments` stores one row per department.
- `department_benefits` stores ordered benefits, one row per benefit, with a
  foreign key and `ON DELETE CASCADE`.

Department reads aggregate benefits in order, so the API still returns
`{"id", "name", "benefits"}`.
