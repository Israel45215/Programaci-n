import flet as ft
import theme


def _stat_card(label, value, value_color):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(label, size=12.5, color=theme.TEXT_SECONDARY),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=value_color),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=theme.PADDING_CARD,
        expand=True,
    )


def build_side_stats() -> ft.Column:
    return ft.Column(
        [
            _stat_card("Total commits", "190", theme.CYAN),
            _stat_card("Total pull requests", "97", theme.PINK),
            _stat_card("Trabajadores", "87", theme.GREEN),
        ],
        spacing=14,
        expand=True,
    )
