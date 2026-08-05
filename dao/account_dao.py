import datetime
import hashlib
import secrets

from database.connection import get_connection

# La tabla "cuentas" (nombre, correo, contrasena, creado_en) guarda las
# cuentas de usuario. La contraseña nunca se guarda en texto plano: se
# guarda como "salt$hash" usando PBKDF2-HMAC-SHA256 (100,000
# iteraciones), la forma estándar de encriptar contraseñas usando solo
# librerías incluidas en Python (hashlib y secrets).


def init_accounts_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            creado_en TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000)
    return f"{salt}${derived.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, derived_hex = stored.split("$", 1)
    except (ValueError, AttributeError):
        return False
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000)
    return secrets.compare_digest(derived.hex(), derived_hex)


def email_exists(correo: str) -> bool:
    init_accounts_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM cuentas WHERE correo = %s", (correo.strip().lower(),))
    row = cursor.fetchone()
    conn.close()
    return row is not None


def create_account(nombre: str, correo: str, contrasena: str):
    """Crea una cuenta nueva.

    Devuelve (True, None) si se creó correctamente, o
    (False, mensaje_de_error) si no se pudo (por ejemplo, correo repetido).
    """
    init_accounts_db()

    nombre = (nombre or "").strip()
    correo_normalizado = (correo or "").strip().lower()

    if not nombre:
        return False, "El nombre es obligatorio."

    if "@" not in correo_normalizado or "." not in correo_normalizado:
        return False, "Ingresa un correo electrónico válido."

    if not contrasena or len(contrasena) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."

    if email_exists(correo_normalizado):
        return False, "Ya existe una cuenta registrada con ese correo."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO cuentas (nombre, correo, contrasena, creado_en)
            VALUES (%s, %s, %s, %s)
        """, (
            nombre,
            correo_normalizado,
            _hash_password(contrasena),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        ))
        conn.commit()
    except Exception:
        conn.rollback()
        conn.close()
        return False, "Ya existe una cuenta registrada con ese correo."

    conn.close()
    return True, None


def validate_login(correo: str, contrasena: str):
    """Valida credenciales contra la tabla 'cuentas'.

    Devuelve el diccionario de la cuenta (sin la contraseña) si el
    correo existe y la contraseña es correcta, o None si no coinciden.
    """
    init_accounts_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, correo, contrasena, creado_en FROM cuentas WHERE correo = %s",
        ((correo or "").strip().lower(),),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    cuenta = dict(row)
    if not _verify_password(contrasena or "", cuenta["contrasena"]):
        return None

    cuenta.pop("contrasena", None)
    return cuenta
