from database.connection import get_connection

# La tabla en Postgres es "metas" (una meta pertenece a un proyecto y,
# opcionalmente, se asigna a un equipo). Los SELECT usan alias en
# inglés para que coincidan con las claves de los modelos y la UI.

_SELECT_COLS = """
    id,
    proyecto_id AS project_id,
    equipo_id AS team_id,
    nombre AS name,
    descripcion AS description,
    estado AS status
"""


def init_pseudo_projects_db():
    from dao.project_dao import init_projects_db
    from dao.team_dao import init_teams_db
    init_projects_db()
    init_teams_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id SERIAL PRIMARY KEY,
            proyecto_id INTEGER NOT NULL REFERENCES proyectos (id),
            equipo_id INTEGER REFERENCES equipos (id),
            nombre TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'Pendiente'
        )
    """)
    conn.commit()
    conn.close()


def get_all_pseudo_projects():
    init_pseudo_projects_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM metas")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_pseudo_projects_by_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM metas WHERE proyecto_id = %s", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_pseudo_projects_by_team(team_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM metas WHERE equipo_id = %s", (team_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_pseudo_project(project_id, team_id, name, description, status="Pendiente"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metas (proyecto_id, equipo_id, nombre, descripcion, estado)
        VALUES (%s, %s, %s, %s, %s)
    """, (project_id, team_id, name, description, status))
    conn.commit()
    conn.close()


def update_pseudo_project(pseudo_id, project_id, team_id, name, description, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE metas
        SET proyecto_id = %s, equipo_id = %s, nombre = %s, descripcion = %s, estado = %s
        WHERE id = %s
    """, (project_id, team_id, name, description, status, pseudo_id))
    conn.commit()
    conn.close()


def delete_pseudo_project(pseudo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metas WHERE id = %s", (pseudo_id,))
    conn.commit()
    conn.close()
