import flet as ft
import theme

def build_metric_card(title: str, subtitle: str, progress: float, color: str, main_value: str, info_text: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=theme.TEXT_SECONDARY),
                        ft.Container(expand=True),
                        ft.Text(main_value, size=18, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    ]
                ),
                ft.Text(subtitle, size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=8),
                ft.ProgressBar(value=progress, color=color, bgcolor=theme.BG_MAIN, height=6, border_radius=3),
                ft.Container(height=4),
                ft.Text(info_text, size=11, color=theme.TEXT_SECONDARY),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=16,
        expand=True,
    )