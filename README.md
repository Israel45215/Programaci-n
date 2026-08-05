# DevTrack

Aplicacion de escritorio para gestion de proyectos, metas, tareas, equipos y empleados, construida con Flet y PostgreSQL.

## Requisitos

- Python 3.10+
- PostgreSQL

## Instalacion

```bash
pip install -r requirements.txt
```

Configura tu conexion en `database/connection.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "devtrack",
    "user": "postgres",
    "password": "TU_CONTRASENA",
}
```

## Uso

```bash
python app.py
```

Las tablas se crean automaticamente la primera vez que la app las necesita.

## Estructura

- `app.py` / `main_window.py` - punto de entrada y ventana principal.
- `ui/` - pantallas e interfaz (login, dashboard, proyectos, metas, tareas, equipos, empleados).
- `models/` - estructura de cada entidad.
- `dao/` - acceso a la base de datos (una consulta SQL por funcion).
- `database/connection.py` - configuracion de conexion a PostgreSQL.
