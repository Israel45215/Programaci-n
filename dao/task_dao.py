from database.connection import get_connection

# La tabla en Postgres es "tareas". Los SELECT usan alias en inglés
# para que coincidan con las claves de los modelos y la UI.

_SELECT_COLS = """
    id,
    titulo AS title,
    meta_id AS pseudo_project_id,
    asignado AS assigned,
    estado AS status,
    prioridad AS priority,
    progreso AS progress,
    fecha_inicio AS start_date,
    fecha_entrega AS date
"""


def init_db():
    from dao.pseudo_project_dao import init_pseudo_projects_db
    init_pseudo_projects_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            meta_id INTEGER REFERENCES metas (id),
            asignado TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            prioridad TEXT DEFAULT 'Media',
            progreso REAL DEFAULT 0.0,
            fecha_inicio TEXT,
            fecha_entrega TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_all_tasks():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM tareas")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_tasks_with_details():
    """
    Igual que get_all_tasks(), pero además trae el nombre de la meta
    y del equipo asignado (vía JOIN), listo para mostrar en la tabla.
    """
    from dao.pseudo_project_dao import init_pseudo_projects_db
    from dao.team_dao import init_teams_db

    init_db()
    init_pseudo_projects_db()
    init_teams_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            t.id,
            t.titulo AS title,
            t.meta_id AS pseudo_project_id,
            t.asignado AS assigned,
            t.estado AS status,
            t.prioridad AS priority,
            t.progreso AS progress,
            t.fecha_inicio AS start_date,
            t.fecha_entrega AS date,
            pp.nombre AS pseudo_project_name,
            pp.equipo_id AS team_id,
            tm.nombre AS team_name
        FROM tareas t
        LEFT JOIN metas pp ON t.meta_id = pp.id
        LEFT JOIN equipos tm ON pp.equipo_id = tm.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_task(title, pseudo_project_id, assigned, status, priority, progress, start_date, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tareas (titulo, meta_id, asignado, estado, prioridad, progreso, fecha_inicio, fecha_entrega)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (title, pseudo_project_id, assigned, status, priority, progress, start_date, date))
    conn.commit()
    conn.close()


def update_task(task_id, title, pseudo_project_id, assigned, status, priority, progress, start_date, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas
        SET titulo = %s, meta_id = %s, asignado = %s, estado = %s, prioridad = %s, progreso = %s, fecha_inicio = %s, fecha_entrega = %s
        WHERE id = %s
    """, (title, pseudo_project_id, assigned, status, priority, progress, start_date, date, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
