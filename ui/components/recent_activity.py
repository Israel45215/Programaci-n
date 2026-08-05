import flet as ft
import theme
from dao.team_dao import get_recent_teams
from dao.project_dao import get_recent_projects, get_finished_projects_by_month
from dao.employee_dao import get_employees_by_team

MONTH_SHORT = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

STATUS_COLORS = {
    "Activo": theme.GREEN,
    "Pausado": "#F59E0B",
    "Finalizado": theme.CYAN,
}


def _status_badge(status: str) -> ft.Container:
    color = STATUS_COLORS.get(status, theme.TEXT_SECONDARY)
    return ft.Container(
        content=ft.Text(status or "Activo", size=10.5, weight=ft.FontWeight.W_600, color=color),
        bgcolor=theme.BG_MAIN,
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
        border_radius=theme.RADIUS_PILL,
    )


def build_recent_teams_card() -> ft.Container:
    teams = get_recent_teams(limit=5)

    if not teams:
        rows = [ft.Text("Aún no hay equipos registrados.", size=12.5, color=theme.TEXT_MUTED)]
    else:
        rows = []
        for t in teams:
            empleados = get_employees_by_team(t["id"])
            members = ", ".join(e["name"] for e in empleados) if empleados else "Sin integrantes asignados"
            rows.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(t["name"], size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                            ft.Text(members, size=11, color=theme.TEXT_MUTED, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ],
                        spacing=2,
                    ),
                    bgcolor=theme.BG_CARD_ALT,
                    padding=10,
                    border_radius=8,
                )
            )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Nuevos equipos", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Últimos equipos creados.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=12),
                ft.Column(rows, spacing=8),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=1,
    )


def build_recent_projects_card() -> ft.Container:
    projects = get_recent_projects(limit=5)

    if not projects:
        rows = [ft.Text("Aún no hay proyectos registrados.", size=12.5, color=theme.TEXT_MUTED)]
    else:
        rows = []
        for p in projects:
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(p["name"], size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                    ft.Text(p.get("technologies") or "Sin tecnologías registradas",
                                            size=11, color=theme.TEXT_MUTED, max_lines=1,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                ],
                                spacing=2, expand=True,
                            ),
                            _status_badge(p.get("status")),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=theme.BG_CARD_ALT,
                    padding=10,
                    border_radius=8,
                )
            )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Nuevos proyectos", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Últimos proyectos creados.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=12),
                ft.Column(rows, spacing=8),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=1,
    )


CHART_HEIGHT = 90


def build_finished_projects_chart() -> ft.Container:
    data = get_finished_projects_by_month(months=6)
    max_count = max((d["count"] for d in data), default=0) or 1

    def bar_column(d):
        bar = ft.Container(
            width=22,
            height=max(3, CHART_HEIGHT * (d["count"] / max_count)),
            bgcolor=theme.ACCENT_COLOR,
            border_radius=4,
            tooltip=f'{MONTH_SHORT[d["month"] - 1]} {d["year"]}: {d["count"]} finalizado(s)',
        )
        return ft.Column(
            [
                ft.Container(content=bar, height=CHART_HEIGHT, alignment=ft.Alignment.BOTTOM_CENTER),
                ft.Text(MONTH_SHORT[d["month"] - 1], size=10, color=theme.TEXT_SECONDARY),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    total_finished = sum(d["count"] for d in data)
    body = (
        ft.Row([bar_column(d) for d in data], spacing=10)
        if total_finished > 0 else
        ft.Text("Aún no hay proyectos finalizados en este periodo.", size=12.5, color=theme.TEXT_MUTED)
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Proyectos finalizados por mes", size=14.5, weight=ft.FontWeight.W_600,
                        color=theme.TEXT_PRIMARY),
                ft.Text("Últimos 6 meses.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=16),
                body,
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=1,
    )
