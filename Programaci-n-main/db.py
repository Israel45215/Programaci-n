"""
Utilidad central para abrir conexiones a PostgreSQL.
Todos los repositorios (proyectos, empleados, tareas, etc.) deben
usar get_connection() para no repetir la configuración en cada archivo.
"""

import psycopg2
import db_config


def get_connection():
    return psycopg2.connect(
        host=db_config.DB_HOST,
        port=db_config.DB_PORT,
        dbname=db_config.DB_NAME,
        user=db_config.DB_USER,
        password=db_config.DB_PASSWORD,
    )
