import flet as ft
import theme


def build_metric_card(title, subtitle, ring_value, ring_color, value_text, value_subtitle):
    """
    Tarjeta con un anillo de progreso tipo 'gauge'.

    ring_value: fracción entre 0 y 1 que llena el anillo.
    value_text: número grande debajo del anillo (ej. '4' o '72%').
    value_subtitle: texto secundario debajo del valor (ej. 'En desarrollo').
    """
    gauge = ft.Stack(
        [
            ft.Container(
                width=88,
                height=88,
                border_radius=44,
                border=ft.Border.all(8, theme.BORDER_SOFT),
            ),
            ft.ProgressRing(
                value=ring_value,
                width=88,
                height=88,
                stroke_width=8,
                color=ring_color,
                bgcolor="transparent",
            ),
        ],
        width=88,
        height=88,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text(title, size=13.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                        ft.Text(subtitle, size=11.5, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=2,
                ),
                ft.Container(height=12),
                ft.Row([gauge], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.Column(
                    [
                        ft.Text(value_text, size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text(value_subtitle, size=11, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=theme.PADDING_CARD,
        expand=True,
    )
