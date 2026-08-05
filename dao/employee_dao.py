from database.connection import get_connection

# La tabla "empleados" (id_empleado, nombre_empleado) guarda el catálogo
# de empleados. La relación "un empleado puede estar en varios equipos"
# vive en la tabla intermedia "empleado_equipo" (muchos a muchos).

_SELECT_COLS = "id_empleado AS id, nombre_empleado AS name"


def init_employees_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado SERIAL PRIMARY KEY,
            nombre_empleado TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def init_employee_team_db():
    from dao.team_dao import init_teams_db
    init_teams_db()
    init_employees_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado_equipo (
            id SERIAL PRIMARY KEY,
            empleado_id INTEGER NOT NULL REFERENCES empleados (id_empleado) ON DELETE CASCADE,
            equipo_id INTEGER NOT NULL REFERENCES equipos (id) ON DELETE CASCADE,
            UNIQUE (empleado_id, equipo_id)
        )
    """)
    conn.commit()
    conn.close()


def get_all_employees():
    init_employees_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {_SELECT_COLS} FROM empleados ORDER BY nombre_empleado")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_employee(name):
    init_employees_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empleados (nombre_empleado) VALUES (%s) RETURNING id_empleado", (name,))
    new_id = cursor.fetchone()["id_empleado"]
    conn.commit()
    conn.close()
    return new_id


def update_employee(employee_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE empleados SET nombre_empleado = %s WHERE id_empleado = %s", (name, employee_id))
    conn.commit()
    conn.close()


def delete_employee(employee_id):
    init_employee_team_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_equipo WHERE empleado_id = %s", (employee_id,))
    cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (employee_id,))
    conn.commit()
    conn.close()


def get_teams_by_employee(employee_id):
    """Todos los equipos en los que está un empleado."""
    init_employee_team_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.nombre AS name
        FROM equipos e
        JOIN empleado_equipo ee ON ee.equipo_id = e.id
        WHERE ee.empleado_id = %s
        ORDER BY e.nombre
    """, (employee_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_employees_by_team(team_id):
    """Todos los empleados que pertenecen a un equipo."""
    init_employee_team_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT emp.id_empleado AS id, emp.nombre_empleado AS name
        FROM empleados emp
        JOIN empleado_equipo ee ON ee.empleado_id = emp.id_empleado
        WHERE ee.equipo_id = %s
        ORDER BY emp.nombre_empleado
    """, (team_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def set_employee_teams(employee_id, team_ids):
    """Reemplaza los equipos asignados a un empleado por la lista
    `team_ids` dada. Como es una relación muchos a muchos, un empleado
    puede quedar asignado a varios equipos a la vez."""
    init_employee_team_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_equipo WHERE empleado_id = %s", (employee_id,))
    for team_id in team_ids:
        cursor.execute(
            "INSERT INTO empleado_equipo (empleado_id, equipo_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (employee_id, team_id),
        )
    conn.commit()
    conn.close()


def set_team_employees(team_id, employee_ids):
    """Reemplaza los empleados asignados a un equipo por la lista
    `employee_ids` dada. Es la misma relación que set_employee_teams,
    pero vista desde el equipo en vez de desde el empleado."""
    init_employee_team_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_equipo WHERE equipo_id = %s", (team_id,))
    for employee_id in employee_ids:
        cursor.execute(
            "INSERT INTO empleado_equipo (empleado_id, equipo_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (employee_id, team_id),
        )
    conn.commit()
    conn.close()
