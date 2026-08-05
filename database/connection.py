import psycopg2
import psycopg2.extras

# Datos de conexión a la base de datos PostgreSQL.
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "devtrack",
    "user": "postgres",
    "password": "CAMBIA_ESTO",
}


def get_connection():
    conn = psycopg2.connect(
        cursor_factory=psycopg2.extras.RealDictCursor,
        **DB_CONFIG,
    )
    conn.set_client_encoding("UTF8")
    return conn
