import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Mapping, Optional

_DB_PATH = Path(__file__).resolve().with_name("projects.db")


def _ensure_parent_directory() -> None:
    if not _DB_PATH.parent.exists():
        _DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Iterable[sqlite3.Connection]:
    _ensure_parent_directory()
    connection = sqlite3.connect(_DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def initialize_database(seed_with_examples: bool = True) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_file_name TEXT NOT NULL,
                detail_slug TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        _ensure_additional_columns(conn)

        if seed_with_examples:
            cursor = conn.execute("SELECT COUNT(1) FROM projects")
            (row_count,) = cursor.fetchone()
            if row_count == 0:
                conn.executemany(
                    """
                    INSERT INTO projects (title, description, image_file_name, detail_slug)
                    VALUES (?, ?, ?, ?)
                    """,
                    [
                        (
                            "Employee Productivity Tracking System",
                            "Teams app that lets employees log tasks, track hours, and monitor productivity KPIs in real time.",
                            "teams-app-screenshot.jpg",
                            "employee-productivity",
                        ),
                        (
                            "ServiceNow AI-Powered Automation",
                            "ServiceNow workflow that uses Google CCAI to transform JSON payloads into rich HTML experiences.",
                            "servicenow-ai-screenshot.jpg",
                            "servicenow-ai",
                        ),
                        (
                            "Power BI KPI Dashboards",
                            "Interactive dashboards that surface executive KPIs with compelling data stories and visuals.",
                            "powerbi-dashboard-screenshot.jpg",
                            "powerbi-dashboard",
                        ),
                        (
                            "SAP Enterprise Solutions Implementation",
                            "SAP GUI build that maps enterprise structure to P2P, OTC, and MTS processes with detailed runbooks.",
                            "sap-gui-screenshot.jpg",
                            "sap-enterprise",
                        ),
                    ],
                )
                conn.commit()
            else:
                _backfill_detail_slugs(conn)


def fetch_all_projects() -> list[Mapping[str, str]]:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, title, description, image_file_name, detail_slug, created_at
            FROM projects
            ORDER BY created_at DESC, id DESC
            """
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def fetch_project_by_id(project_id: int) -> Optional[Mapping[str, str]]:
    """Fetch a single project by its ID."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, title, description, image_file_name, detail_slug, created_at
            FROM projects
            WHERE id = ?
            """,
            (project_id,)
        )
        row = cursor.fetchone()
    return dict(row) if row else None


def insert_project(
    title: str,
    description: str,
    image_file_name: str,
    detail_slug: Optional[str] = None,
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO projects (title, description, image_file_name, detail_slug)
            VALUES (?, ?, ?, ?)
            """,
            (
                title.strip(),
                description.strip(),
                image_file_name.strip(),
                detail_slug.strip() if detail_slug else None,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def delete_project(project_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()


def _ensure_additional_columns(conn: sqlite3.Connection) -> None:
    column_names = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(projects)")
    }
    if "detail_slug" not in column_names:
        conn.execute("ALTER TABLE projects ADD COLUMN detail_slug TEXT")
        conn.commit()


def _backfill_detail_slugs(conn: sqlite3.Connection) -> None:
    fallback_slugs = {
        "Employee Productivity Tracking System": "employee-productivity",
        "ServiceNow AI-Powered Automation": "servicenow-ai",
        "Power BI KPI Dashboards": "powerbi-dashboard",
        "SAP Enterprise Solutions Implementation": "sap-enterprise",
    }
    for title, slug in fallback_slugs.items():
        conn.execute(
            "UPDATE projects SET detail_slug = ? WHERE title = ? AND (detail_slug IS NULL OR detail_slug = '')",
            (slug, title),
        )
    conn.commit()
