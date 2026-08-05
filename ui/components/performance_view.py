import flet as ft
import theme
from dao.team_dao import get_teams_performance
from dao.task_dao import get_all_tasks
from ui.components.team_rating_card import TeamRatingCard


def _metric_card(title, subtitle, value, color, info_text):
    return ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=theme.TEXT_SECONDARY),
                    ft.Container(expand=True),
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ]),
                ft.Text(subtitle, size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=8),
                ft.Text(info_text, size=11, color=color),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=16,
        expand=True,
    )


def _team_rank_row(rank, team):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Text(str(rank), size=13, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    width=28, height=28, bgcolor=theme.BG_CARD_ALT, border_radius=14,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(team["team_name"], size=13.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                        ft.Text(f'{team["completed_tasks"]}/{team["total_tasks"]} tareas completadas',
                                size=11.5, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=2, expand=True,
                ),
                ft.Text(f'{team["score"]:.1f}', size=15, weight=ft.FontWeight.BOLD,
                        color=theme.GREEN if team["score"] >= 7 else theme.TEXT_PRIMARY),
            ],
            spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(vertical=8),
    )


CHART_HEIGHT = 170


def _team_score_chart(teams_with_tasks) -> ft.Container:
    palette = [theme.ACCENT_COLOR, theme.BLUE, theme.CYAN, theme.PURPLE, theme.PINK, theme.GREEN]

    def bar_column(team, color):
        bar = ft.Container(
            width=32,
            height=max(4, CHART_HEIGHT * (team["score"] / 10)),
            bgcolor=color,
            border_radius=6,
            tooltip=f'{team["team_name"]}: {team["score"]:.1f}/10',
        )
        return ft.Column(
            [
                ft.Container(content=bar, height=CHART_HEIGHT, alignment=ft.Alignment.BOTTOM_CENTER),
                ft.Text(team["team_name"], size=10.5, color=theme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                ft.Text(f'{team["score"]:.1f}', size=11, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    columns = [
        bar_column(team, palette[i % len(palette)])
        for i, team in enumerate(teams_with_tasks)
    ]

    body = ft.Row(columns, spacing=16) if columns else ft.Text(
        "Aún no hay tareas asignadas a ningún equipo.", size=13, color=theme.TEXT_SECONDARY
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Score por equipo", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Container(height=18),
                body,
            ],
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=2,
    )


def _status_distribution_chart(tasks) -> ft.Container:
    total = len(tasks) or 1
    counts = {
        "Completada": sum(1 for t in tasks if t["status"] == "Completada"),
        "En Proceso": sum(1 for t in tasks if t["status"] == "En Proceso"),
        "Pendiente": sum(1 for t in tasks if t["status"] == "Pendiente"),
    }
    colors = {"Completada": theme.GREEN, "En Proceso": theme.BLUE, "Pendiente": "#F59E0B"}

    # Barra horizontal apilada: un segmento de color por cada estatus,
    # con ancho proporcional (peso relativo via 'expand').
    segments = []
    for status, count in counts.items():
        if count > 0:
            segments.append(ft.Container(bgcolor=colors[status], expand=count, height=22))
    if not segments:
        segments = [ft.Container(bgcolor=theme.BORDER_SOFT, expand=1, height=22)]

    stacked_bar = ft.Row(segments, spacing=0)

    legend_items = []
    for status, count in counts.items():
        pct = (count / total) * 100
        legend_items.append(
            ft.Row(
                [
                    ft.Container(width=10, height=10, border_radius=5, bgcolor=colors[status]),
                    ft.Text(status, size=12, color=theme.TEXT_SECONDARY),
                    ft.Container(expand=True),
                    ft.Text(f"{count} ({pct:.0f}%)", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ],
                spacing=8,
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Distribución de tareas", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Container(height=14),
                ft.Container(content=stacked_bar, border_radius=8, clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
                ft.Container(height=16),
                ft.Column(legend_items, spacing=10),
            ],
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=1,
    )


def build_performance_view(page: ft.Page) -> ft.Container:
    teams = get_teams_performance()
    tasks = get_all_tasks()

    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "Completada")
    pending = sum(1 for t in tasks if t["status"] == "Pendiente")
    avg_progress = (sum(t["progress"] for t in tasks) / total_tasks * 100) if total_tasks else 0

    teams_with_tasks = [t for t in teams if t["total_tasks"] > 0]
    avg_score = (sum(t["score"] for t in teams_with_tasks) / len(teams_with_tasks)) if teams_with_tasks else 0

    metrics_row = ft.Row(
        [
            _metric_card("Productividad", "Promedio general", f"{avg_progress:.0f}%", theme.GREEN,
                         "Con base en el avance de todas las tareas"),
            _metric_card("Tareas completadas", "Total", str(completed), theme.CYAN,
                         f"de {total_tasks} tareas registradas"),
            _metric_card("Desempeño promedio", "Por equipo", f"{avg_score:.1f}/10", theme.PURPLE,
                         f"{len(teams_with_tasks)} equipos activos"),
            _metric_card("Tareas pendientes", "Por iniciar", str(pending), theme.ERROR_COLOR,
                         "Sin comenzar todavía"),
        ],
        spacing=16,
    )

    ranking_rows = [_team_rank_row(i + 1, team) for i, team in enumerate(teams_with_tasks)] or [
        ft.Text("Aún no hay tareas asignadas a ningún equipo.", size=13, color=theme.TEXT_SECONDARY)
    ]

    ranking_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Ranking de equipos", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Score calculado según el avance promedio de sus tareas.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=6),
                ft.Column(ranking_rows, spacing=2),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
    )

    charts_row = ft.Row(
        [
            _team_score_chart(teams_with_tasks),
            _status_distribution_chart(tasks),
        ],
        spacing=16,
    )

    rating_card = TeamRatingCard(page).build()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Rendimiento", size=24, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ft.Container(height=14),
                metrics_row,
                ft.Container(height=16),
                charts_row,
                ft.Container(height=16),
                ranking_card,
                ft.Container(height=16),
                rating_card,
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )
