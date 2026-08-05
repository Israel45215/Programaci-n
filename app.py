import flet as ft

from main_window import MainWindow
from ui.login import crear_login
from ui.registro import crear_registro
from dao.account_dao import create_account, validate_login


def main(page: ft.Page):
    page.title = "DevTrack"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#050817"

    contenedor_principal = ft.Container(expand=True)

    def mostrar_vista(vista):
        contenedor_principal.content = vista
        page.update()

    def mostrar_login():
        page.title = "DevTrack - Iniciar sesión"
        mostrar_vista(
            crear_login(
                page=page,
                ir_registro=mostrar_registro,
                iniciar_sesion=iniciar_sesion,
            )
        )

    def mostrar_registro():
        page.title = "DevTrack - Crear cuenta"
        mostrar_vista(
            crear_registro(
                page=page,
                volver_login=mostrar_login,
                registrar_usuario=registrar_usuario,
            )
        )

    def mostrar_aplicacion():
        page.title = "DevTrack"
        mostrar_vista(
            MainWindow(
                page=page,
                on_logout=mostrar_login,
            )
        )

    def iniciar_sesion(correo, contrasena, recordar=False):
        cuenta = validate_login(correo, contrasena)
        if cuenta:
            mostrar_aplicacion()
            return True, None
        return False, "Correo o contraseña incorrectos."

    def registrar_usuario(nombre, correo, contrasena):
        exito, error = create_account(nombre, correo, contrasena)
        if exito:
            mostrar_login()
        return exito, error

    page.add(contenedor_principal)
    mostrar_login()


if __name__ == "__main__":
    ft.app(target=main)
