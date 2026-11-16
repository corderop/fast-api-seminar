from app import db

DEPARTMENT_SELECT = """
    SELECT
        d.id,
        d.name,
        COALESCE(
            array_agg(b.benefit ORDER BY b.position)
                FILTER (WHERE b.benefit IS NOT NULL),
            ARRAY[]::text[]
        ) AS benefits
    FROM departments d
    LEFT JOIN department_benefits b ON b.department_id = d.id
"""


def list_departments(benefit: str | None = None) -> list[dict]:
    """Return every department, optionally filtered by one of their benefits."""
    with db.get_connection() as connection:
        if benefit is None or not benefit.strip():
            return connection.execute(
                f"{DEPARTMENT_SELECT} GROUP BY d.id, d.name ORDER BY d.id"
            ).fetchall()

        return connection.execute(
            f"""
            {DEPARTMENT_SELECT}
            WHERE EXISTS (
                SELECT 1
                FROM department_benefits filtered
                WHERE filtered.department_id = d.id
                  AND lower(btrim(filtered.benefit)) = lower(btrim(%s))
            )
            GROUP BY d.id, d.name
            ORDER BY d.id
            """,
            (benefit,),
        ).fetchall()


def find_department(department_id: int) -> dict | None:
    """Return the department with the given id, or None when it does not exist."""
    with db.get_connection() as connection:
        return connection.execute(
            f"{DEPARTMENT_SELECT} WHERE d.id = %s GROUP BY d.id, d.name",
            (department_id,),
        ).fetchone()


def add_department(name: str, benefits: list[str]) -> dict:
    """Create a department and its ordered benefits in one transaction."""
    with db.get_connection() as connection:
        department = connection.execute(
            """
            INSERT INTO departments (name)
            VALUES (%s)
            RETURNING id, name
            """,
            (name,),
        ).fetchone()

        if benefits:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO department_benefits (department_id, position, benefit)
                    VALUES (%s, %s, %s)
                    """,
                    [
                        (department["id"], position, benefit)
                        for position, benefit in enumerate(benefits)
                    ],
                )

    return {
        "id": department["id"],
        "name": department["name"],
        "benefits": list(benefits),
    }
