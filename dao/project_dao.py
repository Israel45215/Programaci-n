import datetime
from database.connection import get_connection

# La tabla en Postgres usa nombres de columna en español ("proyectos"),
# pero los SELECT devuelven las columnas con alias en inglés para que
# coincidan con las claves que usan los modelos y las vistas.

_SELECT_COLS = """
    id,
    nombre AS name,
    descripcion AS description,
    estado AS status,
    tecnologias AS technologies,
    fecha_finalizacion AS finished_at
"""


def init_projects_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'Activo',
            tecnologias TEXT DEFAULT '',
            fecha_finalizacion TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_all_projects():
    init_projects_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM proyectos")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_recent_projects(limit=5):
    """Últimos proyectos creados (los de id más alto primero)."""
    init_projects_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM proyectos ORDER BY id DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_finished_projects_by_month(months=6):
    """Cantidad de proyectos que pasaron a 'Finalizado' por mes,
    para los últimos `months` meses (incluyendo el actual)."""
    init_projects_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha_finalizacion AS finished_at FROM proyectos WHERE fecha_finalizacion IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    counts = {}
    for row in rows:
        month_key = row["finished_at"][:7]  # "YYYY-MM"
        counts[month_key] = counts.get(month_key, 0) + 1

    today = datetime.date.today()
    result = []
    for i in range(months - 1, -1, -1):
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        key = f"{year:04d}-{month:02d}"
        result.append({"month_key": key, "month": month, "year": year, "count": counts.get(key, 0)})
    return result


def get_active_projects_with_upcoming_deadline(limit=6):
    """Proyectos activos ordenados por su fecha límite más próxima.

    La 'fecha límite' de un proyecto no existe como campo propio: se
    calcula como la fecha más lejana entre las tareas de todas sus
    metas (es decir, la fecha en la que, si todo va según lo planeado,
    la última tarea pendiente del proyecto debería quedar completada).
    Solo se consideran proyectos con estado 'Activo' y con fecha
    límite igual o posterior a hoy.
    """
    init_projects_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre AS name, p.estado AS status, MAX(t.fecha_entrega) AS deadline
        FROM proyectos p
        JOIN metas pp ON pp.proyecto_id = p.id
        JOIN tareas t ON t.meta_id = pp.id
        WHERE p.estado = 'Activo' AND t.fecha_entrega IS NOT NULL AND t.fecha_entrega != ''
        GROUP BY p.id, p.nombre, p.estado
        HAVING MAX(t.fecha_entrega) >= to_char(CURRENT_DATE, 'YYYY-MM-DD')
        ORDER BY deadline ASC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_project(name, description, status="Activo", technologies=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO proyectos (nombre, descripcion, estado, tecnologias)
        VALUES (%s, %s, %s, %s)
    """, (name, description, status, technologies))
    conn.commit()
    conn.close()


def update_project(project_id, name, description, status, technologies=""):
    conn = get_connection()
    cursor = conn.cursor()

    if status == "Finalizado":
        cursor.execute("""
            UPDATE proyectos
            SET nombre = %s, descripcion = %s, estado = %s, tecnologias = %s,
                fecha_finalizacion = COALESCE(fecha_finalizacion, %s)
            WHERE id = %s
        """, (name, description, status, technologies,
              datetime.date.today().strftime("%Y-%m-%d"), project_id))
    else:
        cursor.execute("""
            UPDATE proyectos
            SET nombre = %s, descripcion = %s, estado = %s, tecnologias = %s, fecha_finalizacion = NULL
            WHERE id = %s
        """, (name, description, status, technologies, project_id))

    conn.commit()
    conn.close()


def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM metas WHERE proyecto_id = %s", (project_id,))
    pseudo_ids = [row["id"] for row in cursor.fetchall()]

    if pseudo_ids:
        placeholders = ",".join(["%s"] * len(pseudo_ids))
        cursor.execute(f"DELETE FROM tareas WHERE meta_id IN ({placeholders})", pseudo_ids)
        cursor.execute(f"DELETE FROM metas WHERE id IN ({placeholders})", pseudo_ids)

    cursor.execute("DELETE FROM proyectos WHERE id = %s", (project_id,))
    conn.commit()
    conn.close()
