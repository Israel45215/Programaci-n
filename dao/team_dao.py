from database.connection import get_connection
from dao.pseudo_project_dao import init_pseudo_projects_db
from dao.task_dao import init_db

PRIORITY_WEIGHT = {"Alta": 1.5, "Media": 1.0, "Baja": 0.6}

# La tabla en Postgres es "equipos". Los SELECT usan alias en inglés
# para que coincidan con las claves de los modelos y la UI.

_SELECT_COLS = """
    id,
    nombre AS name,
    descripcion AS description,
    miembros AS members
"""


def init_teams_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            miembros TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_all_teams():
    init_teams_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM equipos")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_recent_teams(limit=5):
    """Últimos equipos creados (los de id más alto primero)."""
    init_teams_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM equipos ORDER BY id DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_team_by_id(team_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM equipos WHERE id = %s", (team_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def insert_team(name, description="", members=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equipos (nombre, descripcion, miembros)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, description, members))
    new_id = cursor.fetchone()["id"]
    conn.commit()
    conn.close()
    return new_id


def update_team(team_id, name, description, members):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE equipos SET nombre = %s, descripcion = %s, miembros = %s WHERE id = %s
    """, (name, description, members, team_id))
    conn.commit()
    conn.close()


def delete_team(team_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE metas SET equipo_id = NULL WHERE equipo_id = %s", (team_id,))
    cursor.execute("DELETE FROM equipos WHERE id = %s", (team_id,))
    conn.commit()
    conn.close()


def get_teams_performance():
    """
    Por cada equipo, calcula un score de 0 a 10 combinando:
      - Avance promedio de sus tareas (40%)
      - % de tareas completadas (40%), ponderado por prioridad
      - Volumen de trabajo (20%): equipos con más tareas completadas
        no deberían perder frente a uno con 1 sola tarea al 100%.
    """
    init_teams_db()
    init_pseudo_projects_db()
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            tm.id AS team_id,
            tm.nombre AS team_name,
            t.id AS task_id,
            t.estado AS status,
            t.prioridad AS priority,
            t.progreso AS progress
        FROM equipos tm
        LEFT JOIN metas pp ON pp.equipo_id = tm.id
        LEFT JOIN tareas t ON t.meta_id = pp.id
    """)
    raw_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    teams = {}
    for r in raw_rows:
        team_id = r["team_id"]
        if team_id not in teams:
            teams[team_id] = {
                "team_id": team_id,
                "team_name": r["team_name"],
                "tasks": [],
            }
        if r["task_id"] is not None:
            teams[team_id]["tasks"].append(r)

    max_completed = max(
        (sum(1 for t in team["tasks"] if t["status"] == "Completada") for team in teams.values()),
        default=0,
    )

    results = []
    for team in teams.values():
        tasks = team["tasks"]
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t["status"] == "Completada")

        avg_progress = (sum(t["progress"] or 0.0 for t in tasks) / total_tasks) if total_tasks else 0.0

        if total_tasks:
            weighted_completed = sum(
                PRIORITY_WEIGHT.get(t["priority"], 1.0) for t in tasks if t["status"] == "Completada"
            )
            weighted_total = sum(PRIORITY_WEIGHT.get(t["priority"], 1.0) for t in tasks)
            completion_ratio = weighted_completed / weighted_total if weighted_total else 0.0
        else:
            completion_ratio = 0.0

        volume_ratio = (completed_tasks / max_completed) if max_completed else 0.0

        score = (avg_progress * 0.4 + completion_ratio * 0.4 + volume_ratio * 0.2) * 10

        results.append({
            "team_id": team["team_id"],
            "team_name": team["team_name"],
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "avg_progress": avg_progress,
            "score": round(score, 1),
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results
