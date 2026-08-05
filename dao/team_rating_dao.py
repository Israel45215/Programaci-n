import datetime
from database.connection import get_connection

# La tabla en Postgres es "calificaciones_equipo". Los SELECT usan
# alias en inglés para que coincidan con las claves de los modelos y la UI.

_SELECT_COLS = """
    id,
    equipo_id AS team_id,
    calidad AS quality,
    cumplimiento_plazos AS deadlines,
    comunicacion AS communication,
    colaboracion AS collaboration,
    comentario AS comment,
    creado_en AS created_at
"""


def init_team_ratings_db():
    from dao.team_dao import init_teams_db
    init_teams_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calificaciones_equipo (
            id SERIAL PRIMARY KEY,
            equipo_id INTEGER NOT NULL REFERENCES equipos (id),
            calidad REAL NOT NULL,
            cumplimiento_plazos REAL NOT NULL,
            comunicacion REAL NOT NULL,
            colaboracion REAL NOT NULL,
            comentario TEXT DEFAULT '',
            creado_en TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_team_rating(team_id, quality, deadlines, communication, collaboration, comment=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calificaciones_equipo (equipo_id, calidad, cumplimiento_plazos, comunicacion, colaboracion, comentario, creado_en)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        team_id, quality, deadlines, communication, collaboration, comment,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    ))
    conn.commit()
    conn.close()


def get_ratings_by_team(team_id):
    init_team_ratings_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {_SELECT_COLS} FROM calificaciones_equipo WHERE equipo_id = %s ORDER BY creado_en DESC",
        (team_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_latest_rating_by_team(team_id):
    ratings = get_ratings_by_team(team_id)
    return ratings[0] if ratings else None


def get_latest_ratings_all_teams() -> dict:
    init_team_ratings_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            tr.id,
            tr.equipo_id AS team_id,
            tr.calidad AS quality,
            tr.cumplimiento_plazos AS deadlines,
            tr.comunicacion AS communication,
            tr.colaboracion AS collaboration,
            tr.comentario AS comment,
            tr.creado_en AS created_at
        FROM calificaciones_equipo tr
        INNER JOIN (
            SELECT equipo_id, MAX(creado_en) AS max_date
            FROM calificaciones_equipo
            GROUP BY equipo_id
        ) latest ON tr.equipo_id = latest.equipo_id AND tr.creado_en = latest.max_date
    """)
    rows = cursor.fetchall()
    conn.close()
    return {row["team_id"]: dict(row) for row in rows}


def get_average_score_by_month(months=6):
    init_team_ratings_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT calidad AS quality, cumplimiento_plazos AS deadlines,
               comunicacion AS communication, colaboracion AS collaboration,
               creado_en AS created_at
        FROM calificaciones_equipo
    """)
    rows = cursor.fetchall()
    conn.close()

    sums = {}
    counts = {}
    for row in rows:
        month_key = row["created_at"][:7]
        avg = (row["quality"] + row["deadlines"] + row["communication"] + row["collaboration"]) / 4
        sums[month_key] = sums.get(month_key, 0.0) + avg
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
        avg_score = (sums.get(key, 0.0) / counts[key]) if counts.get(key) else 0.0
        result.append({"month_key": key, "month": month, "year": year, "score": round(avg_score, 1)})
    return result


def delete_team_rating(rating_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calificaciones_equipo WHERE id = %s", (rating_id,))
    conn.commit()
    conn.close()
