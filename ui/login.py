import flet as ft


# =========================================================
# COLORES DE LA INTERFAZ
# Iguales a registro.py
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
# Igual a registro.py
# =========================================================
def crear_logo_devtrack(
    tamano_simbolo: int = 42,
    tamano_texto: int = 34,
):
    return ft.Row(
        controls=[
            ft.Text(
                "<",
                size=tamano_simbolo,
                weight=ft.FontWeight.BOLD,
                color=AZUL_CLARO,
            ),
            ft.Text(
                ">",
                size=tamano_simbolo,
                weight=ft.FontWeight.BOLD,
                color=MORADO_CLARO,
            ),
            ft.Container(width=7),
            ft.Text(
                "DevTrack",
                size=tamano_texto,
                weight=ft.FontWeight.BOLD,
                color=TEXTO_PRINCIPAL,
            ),
        ],
        spacing=0,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


# =========================================================
# PANTALLA DE INICIO DE SESIÓN
# =========================================================
def crear_login(
    page: ft.Page,
    ir_registro=None,
    iniciar_sesion=None,
):
    """
    Crea la pantalla de inicio de sesión.

    ir_registro()
        Cambia a la pantalla de registro.

    iniciar_sesion(correo, contrasena)
        Envía los datos al archivo main.py.
    """

    # =====================================================
    # CAMPOS DEL FORMULARIO
    # Mismos tamaños que registro.py
    # =====================================================
    correo = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo@gmail.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True,
        height=50,
        text_size=14,
        color=TEXTO_PRINCIPAL,
        bgcolor=BG_CAMPO,
        border_color=BORDE,
        focused_border_color=MORADO_CLARO,
        cursor_color=MORADO_CLARO,
        border_radius=10,
        label_style=ft.TextStyle(
            color="#E5E7EB",
            size=13,
        ),
        hint_style=ft.TextStyle(
            color="#697386",
            size=13,
        ),
    )

    contrasena = ft.TextField(
        label="Contraseña",
        hint_text="*************",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        height=50,
        text_size=14,
        color=TEXTO_PRINCIPAL,
        bgcolor=BG_CAMPO,
        border_color=BORDE,
        focused_border_color=MORADO_CLARO,
        cursor_color=MORADO_CLARO,
        border_radius=10,
        label_style=ft.TextStyle(
            color="#E5E7EB",
            size=13,
        ),
        hint_style=ft.TextStyle(
            color="#697386",
            size=13,
        ),
    )

    recordar = ft.Checkbox(
        label="Recordarme",
        value=False,
        active_color=MORADO,
        check_color="#FFFFFF",
        label_style=ft.TextStyle(
            color="#D1D5DB",
            size=12,
        ),
    )

    texto_error = ft.Text(
        value="",
        color=COLOR_ERROR,
        size=12,
        expand=True,
    )

    mensaje_error = ft.Row(
        controls=[
            ft.Icon(
                ft.Icons.ERROR_OUTLINE_ROUNDED,
                color=COLOR_ERROR,
                size=17,
            ),
            texto_error,
        ],
        spacing=7,
        visible=False,
    )

    # =====================================================
    # VALIDACIÓN DEL FORMULARIO
    # =====================================================
    def mostrar_error(texto: str):
        texto_error.value = texto
        mensaje_error.visible = True
        page.update()

    def validar_login(e):
        correo_ingresado = (correo.value or "").strip()
        contrasena_ingresada = contrasena.value or ""

        texto_error.value = ""
        mensaje_error.visible = False

        if not correo_ingresado:
            mostrar_error("Ingresa tu correo electrónico.")
            correo.focus()
            return

        if (
            "@" not in correo_ingresado
            or "." not in correo_ingresado
        ):
            mostrar_error(
                "Ingresa un correo electrónico válido."
            )
            correo.focus()
            return

        if not contrasena_ingresada:
            mostrar_error("Ingresa tu contraseña.")
            contrasena.focus()
            return

        if iniciar_sesion:
            try:
                resultado = iniciar_sesion(
                    correo_ingresado,
                    contrasena_ingresada,
                    recordar.value,
                )
            except TypeError:
                resultado = iniciar_sesion(
                    correo_ingresado,
                    contrasena_ingresada,
                )

            # iniciar_sesion puede devolver (exito, mensaje_error) para
            # avisar si el correo/contraseña no son válidos.
            if isinstance(resultado, tuple):
                exito, error = resultado
                if not exito:
                    mostrar_error(error or "Correo o contraseña incorrectos.")
                    contrasena.focus()

    contrasena.on_submit = validar_login

    # =====================================================
    # BOTÓN INICIAR SESIÓN
    # Mismo tamaño que el botón de registro
    # =====================================================
    boton_login = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.LOGIN_ROUNDED,
                    color="#FFFFFF",
                    size=20,
                ),
                ft.Text(
                    "Iniciar sesión",
                    color="#FFFFFF",
                    size=15,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        height=50,
        alignment=ft.Alignment.CENTER,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=[
                "#7024E8",
                "#A832D7",
                "#D13AC2",
            ],
        ),
        ink=True,
        on_click=validar_login,
    )

    # =====================================================
    # ENLACE PARA CREAR CUENTA
    # =====================================================
    enlace_registro = ft.Row(
        controls=[
            ft.Text(
                "¿No tienes cuenta?",
                color=TEXTO_SECUNDARIO,
                size=13,
            ),
            ft.TextButton(
                content=ft.Text(
                    "Regístrate aquí",
                    color=MORADO_CLARO,
                    size=13,
                    weight=ft.FontWeight.W_600,
                ),
                on_click=(
                    lambda e: ir_registro()
                    if ir_registro
                    else None
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    # =====================================================
    # ETIQUETA SUPERIOR
    # Igual a registro.py
    # =====================================================
    etiqueta_plataforma = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=8,
                    height=8,
                    bgcolor=MORADO_CLARO,
                    border_radius=4,
                ),
                ft.Text(
                    "Plataforma de gestión de proyectos",
                    color="#D7D9E2",
                    size=12,
                ),
            ],
            spacing=8,
        ),
        padding=ft.Padding(
            left=12,
            right=12,
            top=7,
            bottom=7,
        ),
        bgcolor="#10152C",
        border=ft.Border.all(
            1,
            "#202A49",
        ),
        border_radius=18,
    )

    # =====================================================
    # BENEFICIOS
    # Iguales a registro.py
    # =====================================================
    def crear_beneficio(
        icono,
        titulo: str,
        descripcion: str,
        color: str,
        fondo: str,
    ):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icono,
                            color=color,
                            size=24,
                        ),
                        width=52,
                        height=52,
                        bgcolor=fondo,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                color="#FFFFFF",
                                size=13,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Text(
                                descripcion,
                                color=TEXTO_SECUNDARIO,
                                size=10,
                                width=130,
                            ),
                        ],
                        spacing=3,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )

    beneficios = ft.Row(
        controls=[
            crear_beneficio(
                ft.Icons.BOLT_ROUNDED,
                "Más productividad",
                "Optimiza tu tiempo y enfócate en lo importante.",
                "#A855F7",
                "#24155A",
            ),
            crear_beneficio(
                ft.Icons.GROUP_OUTLINED,
                "Colaboración fácil",
                "Trabaja en equipo en tiempo real.",
                "#38BDF8",
                "#11365F",
            ),
            crear_beneficio(
                ft.Icons.SECURITY_ROUNDED,
                "Seguridad total",
                "Tus datos están protegidos.",
                "#2DD4BF",
                "#0D4C4E",
            ),
        ],
        spacing=14,
    )

    # =====================================================
    # PANEL IZQUIERDO
    # Exactamente igual al de crear usuario
    # =====================================================
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
                    (
                        "Crea tu cuenta y comienza a gestionar tus "
                        "proyectos de manera eficiente con DevTrack."
                    ),
                    color="#C7CAD5",
                    size=16,
                    width=610,
                ),

                beneficios,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        expand=15,
        padding=ft.Padding(
            left=55,
            right=40,
            top=22,
            bottom=22,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[
                "#050817",
                "#090A29",
                "#160B42",
                "#080D22",
            ],
        ),
    )

    # =====================================================
    # ENCABEZADO DEL FORMULARIO
    # Mismas dimensiones que registro.py
    # =====================================================
    encabezado_login = ft.Column(
        controls=[
            ft.Container(
                content=ft.Icon(
                    ft.Icons.LOCK_ROUNDED,
                    color="#FFFFFF",
                    size=30,
                ),
                width=70,
                height=70,
                border_radius=35,
                alignment=ft.Alignment.CENTER,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[
                        "#40207C",
                        "#6D28D9",
                    ],
                ),
                shadow=ft.BoxShadow(
                    blur_radius=22,
                    spread_radius=2,
                    color="#443B1B80",
                ),
            ),

            ft.Text(
                "Iniciar sesión",
                color=TEXTO_PRINCIPAL,
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "Bienvenido de nuevo, inicia sesión para continuar",
                color=TEXTO_SECUNDARIO,
                size=13,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=7,
    )

    # =====================================================
    # AVISO INFORMATIVO
    # Ocupa el lugar del aviso de seguridad de registro
    # =====================================================
    aviso_login = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.VERIFIED_USER_ROUNDED,
                    color=MORADO_CLARO,
                    size=21,
                ),
                ft.Text(
                    "Accede de forma segura a tu espacio de trabajo.",
                    color="#E6E7ED",
                    size=12,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=52,
        padding=ft.Padding(
            left=15,
            right=15,
            top=8,
            bottom=8,
        ),
        bgcolor="#11172C",
        border=ft.Border.all(
            1,
            "#3B2B62",
        ),
        border_radius=10,
    )

    # =====================================================
    # FORMULARIO DERECHO
    # Mismo ancho y tamaño exterior que registro.py
    # =====================================================
    ancho_formulario = 465

    formulario = ft.Container(
        content=ft.Column(
            controls=[
                encabezado_login,

                ft.Container(height=5),

                ft.Container(
                    content=correo,
                    width=ancho_formulario,
                ),

                ft.Container(
                    content=contrasena,
                    width=ancho_formulario,
                ),

                ft.Container(
                    content=aviso_login,
                    width=ancho_formulario,
                ),

                ft.Container(
                    content=recordar,
                    width=ancho_formulario,
                ),

                ft.Container(
                    content=mensaje_error,
                    width=ancho_formulario,
                ),

                ft.Container(
                    content=boton_login,
                    width=ancho_formulario,
                ),

                ft.Container(
                    height=1,
                    width=ancho_formulario,
                    bgcolor="#212A42",
                ),

                enlace_registro,
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=560,
        padding=ft.Padding(
            left=45,
            right=45,
            top=22,
            bottom=16,
        ),
        bgcolor=BG_TARJETA,
        border=ft.Border.all(
            1,
            BORDE_MORADO,
        ),
        border_radius=22,
        shadow=ft.BoxShadow(
            blur_radius=35,
            spread_radius=1,
            color="#66000000",
            offset=ft.Offset(0, 12),
        ),
    )

    # =====================================================
    # PANEL DERECHO
    # Igual a registro.py
    # =====================================================
    panel_derecho = ft.Container(
        content=formulario,
        expand=9,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding(
            left=20,
            right=30,
            top=18,
            bottom=18,
        ),
        bgcolor=BG_PRINCIPAL,
    )

    # =====================================================
    # VISTA COMPLETA
    # =====================================================
    return ft.Container(
        content=ft.Row(
            controls=[
                panel_izquierdo,
                panel_derecho,
            ],
            spacing=0,
            expand=True,
        ),
        expand=True,
        bgcolor=BG_PRINCIPAL,
    )
