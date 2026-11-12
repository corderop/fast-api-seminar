def getNextId(departments: list[dict]) -> int:
    """Return the next available department id."""
    return max((department["id"] for department in departments), default=0) + 1
