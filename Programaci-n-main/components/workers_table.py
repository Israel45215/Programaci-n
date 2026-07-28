import flet as ft
import theme

NEW_WORKERS = [
    {"name": "Rubén", "phone": "(718) 400-2200"},
    {"name": "Doreen", "phone": "(607) 851-1234"},
    {"name": "Ana", "phone": "(808) 887-0787"},
    {"name": "Green", "phone": "(202) 555-0198"},
    {"name": "Devlin", "phone": "(272) 828-5980"},
]


def _worker_row(name, phone):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, size=16, color="#FFFFFF"),
                    width=32,
                    height=32,
                    border_radius=16,
                    bgcolor=theme.INDIGO,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text(name, size=13, color=theme.TEXT_PRIMARY, width=110),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CALL_ROUNDED, size=14, color=theme.TEXT_MUTED),
                        ft.Text(phone, size=12.5, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=6,
                ),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.MORE_HORIZ_ROUNDED, size=18, color=theme.TEXT_MUTED),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.BG_CARD_ALT,
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=10,
    )


def _page_button(label, active=False):
    return ft.Container(
        content=ft.Text(str(label), size=12.5, color="#FFFFFF" if active else theme.TEXT_SECONDARY),
        width=28,
        height=28,
        border_radius=14,
        bgcolor=theme.INDIGO if active else "transparent",
        alignment=ft.Alignment.CENTER,
        ink=True,
    )


def build_workers_table() -> ft.Container:
    header = ft.Row(
        [
            ft.Text("Nuevos Trabajadores", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Recientes", size=12, color=theme.TEXT_SECONDARY),
                        ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=15, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=4,
                ),
                bgcolor=theme.BG_INPUT,
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                border_radius=theme.RADIUS_PILL,
            ),
            ft.Container(width=10),
            ft.Text("Ver todo", size=12.5, color=theme.INDIGO, weight=ft.FontWeight.W_600),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    rows = ft.Column(
        [_worker_row(w["name"], w["phone"]) for w in NEW_WORKERS],
        spacing=8,
    )

    pagination = ft.Row(
        [_page_button(1, active=True), _page_button(2), _page_button(3), _page_button(4)],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=6,
    )

    return ft.Container(
        content=ft.Column([header, ft.Container(height=14), rows, ft.Container(height=10), pagination]),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=theme.PADDING_CARD,
        expand=True,
    )
