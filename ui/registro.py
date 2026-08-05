import flet as ft


# =========================================================
# COLORES DE LA INTERFAZ
# =========================================================
BG_PRINCIPAL = "#050817"
BG_TARJETA = "#090E20"
BG_CAMPO = "#0D1429"

AZUL_CLARO = "#22D3EE"
MORADO = "#7C3AED"
MORADO_CLARO = "#A855F7"

TEXTO_PRINCIPAL = "#FFFFFF"
TEXTO_SECUNDARIO = "#AAB1C3"
BORDE = "#28324D"
BORDE_MORADO = "#7137D8"
COLOR_ERROR = "#F87171"


# =========================================================
# LOGOTIPO DEVTRACK
# =========================================================
def crear_logo_devtrack(
    tamano_simbolo: int = 42,
    tamano_texto: int = 34,
):
    return ft.Row(
        controls=[
            ft.Text("<", size=tamano_simbolo, weight=ft.FontWeight.BOLD, color=AZUL_CLARO),
            ft.Text(">", size=tamano_simbolo, weight=ft.FontWeight.BOLD, color=MORADO_CLARO),
            ft.Container(width=7),
            ft.Text("DevTrack", size=tamano_texto, weight=ft.FontWeight.BOLD, color=TEXTO_PRINCIPAL),
        ],
        spacing=0,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# =========================================================
# PANTALLA DE REGISTRO
# =========================================================
def crear_registro(
    page: ft.Page,
    volver_login=None,
    registrar_usuario=None,
):
    # =====================================================
    # CAMPOS DEL FORMULARIO
    # =====================================================
    def campo_base(**kwargs):
        return ft.TextField(
            height=50,
            text_size=14,
            color=TEXTO_PRINCIPAL,
            bgcolor=BG_CAMPO,
            border_color=BORDE,
            focused_border_color=MORADO_CLARO,
            cursor_color=MORADO_CLARO,
            border_radius=10,
            label_style=ft.TextStyle(color="#E5E7EB", size=13),
            hint_style=ft.TextStyle(color="#697386", size=13),
            **kwargs,
        )

    nombre = campo_base(
        label="Nombre completo",
        hint_text="Escribe tu nombre completo",
        prefix_icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
        autofocus=True,
    )

    correo = campo_base(
        label="Correo electrónico",
        hint_text="ejemplo@gmail.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
    )

    contrasena = campo_base(
        label="Contraseña",
        hint_text="*************",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
    )

    confirmar_contrasena = campo_base(
        label="Confirmar contraseña",
        hint_text="*************",
        prefix_icon=ft.Icons.LOCK_RESET_ROUNDED,
        password=True,
        can_reveal_password=True,
    )

    texto_requisito = ft.Text(
        "La contraseña debe tener mínimo 6 caracteres.",
        color=TEXTO_SECUNDARIO,
        size=11,
    )

    aceptar_terminos = ft.Checkbox(
        value=False,
        active_color=MORADO,
        check_color="#FFFFFF",
        label="Acepto los términos y condiciones y la política de privacidad",
        label_style=ft.TextStyle(color="#D1D5DB", size=12),
    )

    texto_error = ft.Text("", color=COLOR_ERROR, size=12, expand=True)
    mensaje_error = ft.Row(
        controls=[
            ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, color=COLOR_ERROR, size=17),
            texto_error,
        ],
        spacing=7,
        visible=False,
    )

    # =====================================================
    # VALIDACIÓN
    # =====================================================
    def mostrar_error(texto: str):
        texto_error.value = texto
        mensaje_error.visible = True
        page.update()

    def validar_registro(e):
        nombre_ingresado = (nombre.value or "").strip()
        correo_ingresado = (correo.value or "").strip()
        contrasena_ingresada = contrasena.value or ""
        confirmacion_ingresada = confirmar_contrasena.value or ""

        texto_error.value = ""
        mensaje_error.visible = False

        if not nombre_ingresado:
            mostrar_error("Ingresa tu nombre completo.")
            nombre.focus()
            return

        if len(nombre_ingresado) < 3:
            mostrar_error("El nombre debe tener al menos 3 caracteres.")
            nombre.focus()
            return

        if not correo_ingresado:
            mostrar_error("Ingresa tu correo electrónico.")
            correo.focus()
            return

        if "@" not in correo_ingresado or "." not in correo_ingresado:
            mostrar_error("Ingresa un correo electrónico válido.")
            correo.focus()
            return

        if not contrasena_ingresada:
            mostrar_error("Ingresa una contraseña.")
            contrasena.focus()
            return

        if len(contrasena_ingresada) < 6:
            mostrar_error("La contraseña debe tener mínimo 6 caracteres.")
            contrasena.focus()
            return

        if not confirmacion_ingresada:
            mostrar_error("Confirma tu contraseña.")
            confirmar_contrasena.focus()
            return

        if contrasena_ingresada != confirmacion_ingresada:
            mostrar_error("Las contraseñas no coinciden.")
            confirmar_contrasena.focus()
            return

        if not aceptar_terminos.value:
            mostrar_error("Debes aceptar los términos y condiciones.")
            return

        if registrar_usuario:
            resultado = registrar_usuario(nombre_ingresado, correo_ingresado, contrasena_ingresada)

            # registrar_usuario puede devolver (exito, mensaje_error) para
            # avisar si, por ejemplo, el correo ya está registrado.
            if isinstance(resultado, tuple):
                exito, error = resultado
                if not exito:
                    mostrar_error(error or "No se pudo crear la cuenta.")
                    correo.focus()

    confirmar_contrasena.on_submit = validar_registro

    # =====================================================
    # BOTÓN Y ENLACE
    # =====================================================
    boton_registro = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color="#FFFFFF", size=20),
                ft.Text("Crear cuenta", size=15, weight=ft.FontWeight.W_600, color="#FFFFFF"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        height=50,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=["#7024E8", "#A832D7", "#D13AC2"],
        ),
        ink=True,
        on_click=validar_registro,
    )

    enlace_login = ft.Row(
        controls=[
            ft.Text("¿Ya tienes cuenta?", color=TEXTO_SECUNDARIO, size=13),
            ft.TextButton(
                content=ft.Text(
                    "Inicia sesión aquí",
                    color=MORADO_CLARO,
                    size=13,
                    weight=ft.FontWeight.W_600,
                ),
                on_click=lambda e: volver_login() if volver_login else None,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    # =====================================================
    # LADO IZQUIERDO: IGUAL AL LOGIN
    # =====================================================
    etiqueta_plataforma = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(width=8, height=8, bgcolor=MORADO_CLARO, border_radius=4),
                ft.Text("Plataforma de gestión de proyectos", color="#D7D9E2", size=12),
            ],
            spacing=8,
            tight=True,
        ),
        padding=ft.Padding(left=12, right=12, top=7, bottom=7),
        bgcolor="#10152C",
        border=ft.Border.all(1, "#202A49"),
        border_radius=18,
    )

    def crear_beneficio(icono, titulo, descripcion, color_icono, color_fondo):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, color=color_icono, size=24),
                        width=51,
                        height=51,
                        bgcolor=color_fondo,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(titulo, color="#FFFFFF", size=12, weight=ft.FontWeight.W_600),
                            ft.Text(descripcion, color=TEXTO_SECUNDARIO, size=9, width=125),
                        ],
                        spacing=3,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=75,
            padding=ft.Padding(left=10, right=10, top=9, bottom=9),
            bgcolor="#0D1329",
            border=ft.Border.all(1, "#222D4A"),
            border_radius=12,
            expand=True,
        )

    beneficios = ft.Row(
        controls=[
            crear_beneficio(
                ft.Icons.BOLT_ROUNDED,
                "Más productividad",
                "Optimiza tu tiempo y enfócate en lo importante.",
                "#C026FF",
                "#261451",
            ),
            crear_beneficio(
                ft.Icons.GROUP_ROUNDED,
                "Colaboración fácil",
                "Trabaja en equipo en tiempo real.",
                "#1FC8FF",
                "#0B3158",
            ),
            crear_beneficio(
                ft.Icons.SECURITY_ROUNDED,
                "Seguridad total",
                "Tus datos están protegidos.",
                "#17E6A1",
                "#0B403D",
            ),
        ],
        spacing=11,
    )

    panel_izquierdo = ft.Container(
        content=ft.Column(
            controls=[
                crear_logo_devtrack(),
                etiqueta_plataforma,
                ft.Text(
                    "Organiza. Colabora.",
                    color=TEXTO_PRINCIPAL,
                    size=42,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Entrega resultados.",
                    color=MORADO_CLARO,
                    size=44,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Gestiona proyectos, organiza tareas y colabora con tu equipo desde un solo lugar.",
                    color="#C7CAD5",
                    size=16,
                    width=610,
                ),
                beneficios,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=9,
        ),
        expand=15,
        padding=ft.Padding(left=55, right=40, top=22, bottom=22),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#040716", "#070A24", "#130A3D", "#071126"],
        ),
    )

    # =====================================================
    # PANEL DERECHO DE REGISTRO
    # =====================================================
    encabezado_formulario = ft.Column(
        controls=[
            ft.Container(
                content=ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color="#FFFFFF", size=30),
                width=70,
                height=70,
                border_radius=35,
                alignment=ft.Alignment.CENTER,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=["#40207C", "#6D28D9"],
                ),
                shadow=ft.BoxShadow(blur_radius=22, spread_radius=2, color="#443B1B80"),
            ),
            ft.Text(
                "Crear cuenta",
                color=TEXTO_PRINCIPAL,
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Completa tus datos para comenzar",
                color=TEXTO_SECUNDARIO,
                size=13,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=7,
    )

    aviso_seguridad = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.SECURITY_ROUNDED, color=MORADO_CLARO, size=21),
                ft.Text(
                    "Tus datos están protegidos con encriptación avanzada.",
                    color="#E6E7ED",
                    size=12,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=52,
        padding=ft.Padding(left=15, right=15, top=8, bottom=8),
        bgcolor="#11172C",
        border=ft.Border.all(1, "#3B2B62"),
        border_radius=10,
    )

    ancho_formulario = 465

    formulario = ft.Container(
        content=ft.Column(
            controls=[
                encabezado_formulario,
                ft.Container(height=5),
                ft.Container(content=nombre, width=ancho_formulario),
                ft.Container(content=correo, width=ancho_formulario),
                ft.Container(content=contrasena, width=ancho_formulario),
                ft.Container(content=texto_requisito, width=ancho_formulario),
                ft.Container(content=confirmar_contrasena, width=ancho_formulario),
                ft.Container(content=aviso_seguridad, width=ancho_formulario),
                ft.Container(content=aceptar_terminos, width=ancho_formulario),
                ft.Container(content=mensaje_error, width=ancho_formulario),
                ft.Container(content=boton_registro, width=ancho_formulario),
                ft.Container(height=1, width=ancho_formulario, bgcolor="#212A42"),
                enlace_login,
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=560,
        padding=ft.Padding(left=45, right=45, top=22, bottom=16),
        bgcolor=BG_TARJETA,
        border=ft.Border.all(1, BORDE_MORADO),
        border_radius=22,
        shadow=ft.BoxShadow(
            blur_radius=35,
            spread_radius=1,
            color="#66000000",
            offset=ft.Offset(0, 12),
        ),
    )

    panel_derecho = ft.Container(
        content=formulario,
        expand=9,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding(left=20, right=30, top=18, bottom=18),
        bgcolor=BG_PRINCIPAL,
    )

    return ft.Container(
        content=ft.Row(
            controls=[panel_izquierdo, panel_derecho],
            spacing=0,
            expand=True,
        ),
        expand=True,
        bgcolor=BG_PRINCIPAL,
    )
