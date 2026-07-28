import flet as ft
import theme


def build_topbar() -> ft.Container:
    """Construye la barra superior (Topbar) con avatar de perfil."""

    # Campo de búsqueda global
    search_input = ft.TextField(
        hint_text="Buscar en DevTrack...",
        hint_style=ft.TextStyle(color=theme.TEXT_MUTED, size=13),
        border_radius=20,
        bgcolor=theme.BG_INPUT,
        border_color="transparent",
        focused_border_color=theme.INDIGO,
        content_padding=ft.Padding.only(left=15, right=15, top=10, bottom=10),
        text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        height=40,
    )

    # Avatar de usuario / Foto de perfil circular
    user_avatar = ft.Container(
        content=ft.CircleAvatar(
            content=ft.Icon(ft.Icons.PERSON, size=18, color="#FFFFFF"),
            bgcolor=theme.INDIGO,
            radius=16,
        ),
        margin=ft.Margin.only(left=8),
        tooltip="Mi Perfil",
    )

    # Botones de acción derecha (Notificaciones, Calendario y Foto de Perfil)
    actions = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                icon_color=theme.TEXT_SECONDARY,
                tooltip="Notificaciones",
            ),
            ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                icon_color=theme.TEXT_SECONDARY,
                tooltip="Calendario",
            ),
            user_avatar,  # 👈 Círculo de perfil a la derecha
        ],
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Row(
            [
                ft.Container(content=search_input, width=320),
                ft.Container(expand=True),
                actions,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=28, vertical=12),
        border=ft.Border(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
        bgcolor=theme.BG_PAGE,
    )