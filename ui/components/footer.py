import flet as ft
import theme


def build_footer(page: ft.Page = None) -> ft.Container:
    logo = ft.Row(
        [
            ft.Container(
                width=24,
                height=24,
                bgcolor=theme.ACCENT_COLOR,
                border_radius=6,
                content=ft.Icon(ft.Icons.CODE, color="#FFFFFF", size=14),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Text("© 2026 DevTrack", size=12.5, color=theme.TEXT_SECONDARY),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def footer_link(label: str):
        return ft.Text(
            label,
            size=12.5,
            color=theme.TEXT_SECONDARY,
        )

    links = ft.Row(
        [
            footer_link("Ayuda"),
            ft.Text("|", size=12.5, color=theme.BORDER_SOFT),
            footer_link("Documentación"),
            ft.Text("|", size=12.5, color=theme.BORDER_SOFT),
            footer_link("Reportar un error"),
            ft.Text("|", size=12.5, color=theme.BORDER_SOFT),
            footer_link("Contacto"),
        ],
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    team_note = ft.Text(
        "Proyecto académico — 3er cuatrimestre",
        size=12,
        color=theme.TEXT_MUTED,
    )

    return ft.Container(
        content=ft.Row(
            [
                logo,
                ft.Container(expand=True),
                links,
                ft.Container(expand=True),
                team_note,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.BG_SIDEBAR,
        padding=ft.Padding.symmetric(horizontal=28, vertical=12),
        border=ft.Border(top=ft.BorderSide(1, theme.BORDER_SOFT)),
    )