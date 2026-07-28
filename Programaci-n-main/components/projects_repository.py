"""
Repositorio de acceso a datos para la tabla public.proyectos.

Columnas reales en la base de datos:
    id_proyecto     integer, PK, autogenerado
    nombre_proyecto varchar(30)
    fecha_inicio    date
    fecha_entrega   date

Hacia la vista (Flet) exponemos diccionarios con:
    id          -> id_proyecto (int), se usa para editar/borrar
    display_id  -> "PRJ-001" (solo para mostrar en la tabla)
    name        -> nombre_proyecto
    start       -> fecha_inicio formateada como día/mes/año
    end         -> fecha_entrega formateada como día/mes/año
"""

import datetime
from db import get_connection


def _to_display(row):
    project_id, name, start, end = row
    return {
        "id": project_id,
        "display_id": f"PRJ-{project_id:03d}",
        "name": name,
        "start": start.strftime("%d/%m/%Y") if start else "",
        "end": end.strftime("%d/%m/%Y") if end else "",
    }


def _parse_date(date_str: str) -> datetime.date:
    """Convierte 'día/mes/año' (o con guiones) a un objeto date de Python."""
    date_str = (date_str or "").strip()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Fecha inválida: '{date_str}'. Usa el formato día/mes/año, ej. 15/12/2023.")


def fetch_all():
    """Devuelve todos los proyectos ordenados por id_proyecto."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_proyecto, nombre_proyecto, fecha_inicio, fecha_entrega "
                "FROM public.proyectos ORDER BY id_proyecto ASC"
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [_to_display(row) for row in rows]


def create(name: str, start_str: str, end_str: str) -> int:
    """Inserta un nuevo proyecto y devuelve el id_proyecto generado."""
    start_date = _parse_date(start_str)
    end_date = _parse_date(end_str)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO public.proyectos (nombre_proyecto, fecha_inicio, fecha_entrega) "
                "VALUES (%s, %s, %s) RETURNING id_proyecto",
                (name, start_date, end_date),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
    finally:
        conn.close()
    return new_id


def update(project_id: int, name: str, start_str: str, end_str: str):
    """Actualiza un proyecto existente por su id_proyecto."""
    start_date = _parse_date(start_str)
    end_date = _parse_date(end_str)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE public.proyectos "
                "SET nombre_proyecto = %s, fecha_inicio = %s, fecha_entrega = %s "
                "WHERE id_proyecto = %s",
                (name, start_date, end_date, project_id),
            )
        conn.commit()
    finally:
        conn.close()


def delete(project_id: int):
    """Elimina un proyecto por su id_proyecto."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.proyectos WHERE id_proyecto = %s", (project_id,))
        conn.commit()
    finally:
        conn.close()
