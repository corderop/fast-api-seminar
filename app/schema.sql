CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS departments (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS department_benefits (
    department_id BIGINT NOT NULL REFERENCES departments (id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    benefit TEXT NOT NULL,
    PRIMARY KEY (department_id, position)
);

CREATE INDEX IF NOT EXISTS department_benefits_benefit_idx
    ON department_benefits (lower(btrim(benefit)));
