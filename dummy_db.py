from __future__ import annotations

from sqlalchemy import text

from database import engine

def run_sql(query: str):
    """Run a raw SQL query against the database used by database.py
    Example: 
        rows = run_sql("SELECT * FROM appointments")
        print(rows)  
    """
    with engine.begin() as conn:
        result  = conn.execute(text(query))
        return result.fetchall() if result.returns_rows else result.rowcount


# query = "INSERT INTO appointments (patient_name, reason, start_time) VALUES ('John Doe', 'Routine Checkup', '2024-06-15 10:00:00')"
query = "SELECT * FROM appointments"
print(run_sql(query))


