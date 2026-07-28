import flet as ft
import theme


def _nav_item(icon, label, route, selected_route, on_click, badge=None):
    """Construye un item de navegación individual del sidebar."""
    is_active = route == selected_route

    content_row = [
        ft.Icon(
            icon,
            size=19,
            color=theme.TEXT_PRIMARY if is_active else theme.TEXT_SECONDARY,
        ),
        ft.Text(
            label,
            size=13.5,
            weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
            color=theme.TEXT_PRIMARY if is_active else theme.TEXT_SECONDARY,
        ),
    ]

    if badge:
        content_row.append(
            ft.Container(expand=True),
        )
        content_row.append(
            ft.Container(
                content=ft.Text(str(badge), size=10, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                bgcolor="#EF4444",
                width=18,
                height=18,
                border_radius=9,
                alignment=ft.Alignment.CENTER,
            )
        )

    return ft.Container(
        content=ft.Row(content_row, spacing=12),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=10,
        bgcolor=theme.SIDEBAR_ACTIVE_BG if is_active else None,
        on_click=lambda e: on_click(route),
        ink=True,
        animate=150,
    )


def _section_label(text_value):
    return ft.Container(
        content=ft.Text(
            text_value.upper(),
            size=10.5,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT_MUTED,
        ),
        padding=ft.Padding.only(left=14, top=16, bottom=4),
    )


def build_sidebar(selected_route: str, on_navigate) -> ft.Container:
    """
    Sidebar de navegación completo.

    selected_route: clave de la ruta activa (ej. "dashboard").
    on_navigate: callback(route) invocado al hacer click en un item.
    """

    logo = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, color="#FFFFFF", size=18),
                    width=34,
                    height=34,
                    border_radius=10,
                    gradient=ft.LinearGradient(
                        colors=[theme.INDIGO, theme.PURPLE],
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                    ),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text("DevTrack", size=18, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
            ],
            spacing=10,
        ),
        padding=ft.Padding.only(left=16, top=18, bottom=10),
    )

    main_items = ft.Column(
        [
            _nav_item(ft.Icons.GRID_VIEW_ROUNDED, "Dashboard", "dashboard", selected_route, on_navigate),
            _nav_item(ft.Icons.FOLDER_COPY_ROUNDED, "Proyectos", "proyectos", selected_route, on_navigate),
        ],
        spacing=4,
    )

    reportes_items = ft.Column(
        [
            _section_label("Reportes"),
            _nav_item(ft.Icons.TASK_ALT_ROUNDED, "Tareas", "tareas", selected_route, on_navigate),
            _nav_item(ft.Icons.GROUPS_ROUNDED, "Empleados", "empleados", selected_route, on_navigate),
            _nav_item(ft.Icons.INSIGHTS_ROUNDED, "Rendimiento", "rendimiento", selected_route, on_navigate),
        ],
        spacing=4,
    )

    personal_items = ft.Column(
        [
            _section_label("Personal"),
            _nav_item(ft.Icons.CALENDAR_MONTH_ROUNDED, "Calendario", "calendario", selected_route, on_navigate),
            _nav_item(ft.Icons.CHAT_BUBBLE_ROUNDED, "Mensajes", "mensajes", selected_route, on_navigate, badge=3),
            _nav_item(ft.Icons.SETTINGS_ROUNDED, "Ajustes", "ajustes", selected_route, on_navigate),
            _nav_item(ft.Icons.SUMMARIZE_ROUNDED, "Reporte", "reporte", selected_route, on_navigate),
        ],
        spacing=4,
    )

    logout = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=theme.TEXT_SECONDARY, size=19)],
        ),
        padding=ft.Padding.only(left=14, bottom=16, top=10),
        on_click=lambda e: on_navigate("logout"),
        ink=True,
        border_radius=10,
    )

    return ft.Container(
        content=ft.Column(
            [
                logo,
                ft.Container(
                    content=ft.Column([main_items, reportes_items, personal_items], spacing=0),
                    padding=ft.Padding.symmetric(horizontal=8),
                    expand=True,
                ),
                logout,
            ],
            spacing=0,
        ),
        width=theme.SIDEBAR_WIDTH,
        bgcolor=theme.BG_SIDEBAR,
        border=ft.Border.only(right=ft.BorderSide(1, theme.BORDER_SOFT)),
    )
