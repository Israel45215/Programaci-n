import flet as ft
import theme
from components.metric_card import build_metric_card
from components.commits_chart import build_commits_chart
from components.side_stats import build_side_stats
from components.workers_table import build_workers_table
from components.mini_calendar import build_mini_calendar


def _section_header() -> ft.Row:
    return ft.Row(
        [
            ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
        ]
    )


def _summary_toolbar() -> ft.Row:
    return ft.Row(
        [
            ft.Container(
                content=ft.Text("Resumen general", size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                bgcolor=theme.BG_CARD,
                padding=ft.Padding.symmetric(horizontal=16, vertical=9),
                border_radius=theme.RADIUS_PILL,
            ),
            ft.Container(expand=True),
            ft.Icon(ft.Icons.MORE_HORIZ_ROUNDED, size=20, color=theme.TEXT_SECONDARY),
        ]
    )


def build_dashboard_view() -> ft.Container:
    metrics_row = ft.Row(
        [
            build_metric_card("Proyectos", "Activos", 0.8, theme.GREEN, "4", "En desarrollo"),
            build_metric_card("Pago", "Pendientes", 0.55, theme.BLUE, "9", "Por resolver"),
            build_metric_card("Commits", "Realización", 0.72, theme.BLUE, "72%", "+12% por mes"),
            build_metric_card("Pull Requests", "Creados", 0.80, theme.PURPLE, "80%", "+8% por mes"),
        ],
        spacing=16,
    )

    charts_row = ft.Row(
        [
            ft.Container(content=build_commits_chart(), expand=3),
            ft.Container(content=build_side_stats(), expand=1),
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    tables_row = ft.Row(
        [
            ft.Container(content=build_workers_table(), expand=3),
            ft.Container(content=build_mini_calendar(), expand=1),
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    return ft.Container(
        content=ft.Column(
            [
                _section_header(),
                ft.Container(height=14),
                _summary_toolbar(),
                ft.Container(height=16),
                metrics_row,
                ft.Container(height=16),
                charts_row,
                ft.Container(height=16),
                tables_row,
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.Padding.only(left=28, right=28, bottom=24),
        expand=True,
    )
