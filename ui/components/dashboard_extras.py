import flet as ft
import theme
from dao.project_dao import get_recent_projects, get_active_projects_with_upcoming_deadline
from dao.pseudo_project_dao import get_pseudo_projects_by_project
from dao.team_rating_dao import get_average_score_by_month

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


# ---------- Tabla de nuevos proyectos ----------

def _projects_table_header() -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Text("Proyecto", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, expand=2),
                ft.Text("Tecnologías", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, expand=2),
                ft.Text("Pseudo-proy.", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED,
                        width=90, text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Text("Estado", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED,
                                     text_align=ft.TextAlign.CENTER),
                    width=90,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border=ft.Border(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
    )


def _project_row(p: dict) -> ft.Container:
    techs = (p.get("technologies") or "").replace(",", ", ")
    pseudo_count = len(get_pseudo_projects_by_project(p["id"]))

    return ft.Container(
        content=ft.Row(
            [
                ft.Text(p["name"], size=12.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY, expand=2),
                ft.Text(techs or "Sin tecnologías", size=11.5, color=theme.TEXT_MUTED, expand=2,
                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Text(str(pseudo_count), size=12, color=theme.TEXT_SECONDARY,
                        width=90, text_align=ft.TextAlign.CENTER),
                ft.Container(content=_status_badge(p.get("status")), width=90, alignment=ft.Alignment.CENTER),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        bgcolor=theme.BG_CARD_ALT,
        border_radius=8,
    )


def build_new_projects_table(limit=6) -> ft.Container:
    """Tabla con los proyectos creados más recientemente."""
    projects = get_recent_projects(limit=limit)

    if not projects:
        body = ft.Container(
            content=ft.Text("Aún no hay proyectos registrados.", size=12.5, color=theme.TEXT_MUTED),
            padding=16,
        )
    else:
        body = ft.Column(
            [_projects_table_header(), ft.Container(height=6), *[_project_row(p) for p in projects]],
            spacing=6,
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Nuevos proyectos", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Últimos proyectos creados.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=12),
                body,
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=2,
    )


# ---------- Mini calendario: proyectos por finalizar ----------

def build_project_deadlines_calendar(limit=5) -> ft.Container:
    """Mini calendario con las fechas límite (calculadas a partir de las
    tareas de sus metas) de los proyectos activos que están
    más cerca de terminar."""
    projects = get_active_projects_with_upcoming_deadline(limit=limit)

    if not projects:
        items = [ft.Text("No hay proyectos activos con fecha límite próxima.", size=12, color=theme.TEXT_MUTED)]
    else:
        items = []
        for p in projects:
            items.append(
                ft.Row(
                    [
                        ft.Container(width=6, height=6, border_radius=3, bgcolor=theme.ACCENT_COLOR),
                        ft.Column(
                            [
                                ft.Text(p["name"], size=12, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                ft.Text(p["deadline"], size=10.5, color=theme.TEXT_SECONDARY),
                            ],
                            spacing=1, expand=True,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Proyectos por finalizar", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Según la fecha límite de sus tareas.", size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=10),
                ft.Column(items, spacing=10),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=1,
    )


# ---------- Gráfica mensual: rendimiento de equipos ----------

CHART_HEIGHT = 90


def build_team_performance_chart() -> ft.Container:
    """Gráfica mensual con el promedio (0-10) de las calificaciones de
    equipos registradas en los últimos 6 meses."""
    data = get_average_score_by_month(months=6)
    max_score = max((d["score"] for d in data), default=0) or 10

    def bar_column(d):
        bar = ft.Container(
            width=22,
            height=max(3, CHART_HEIGHT * (d["score"] / max_score)) if d["score"] > 0 else 3,
            bgcolor=theme.PURPLE,
            border_radius=4,
            tooltip=f'{MONTH_SHORT[d["month"] - 1]} {d["year"]}: {d["score"]:.1f}/10',
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

    total_ratings = sum(1 for d in data if d["score"] > 0)
    body = (
        ft.Row([bar_column(d) for d in data], spacing=10)
        if total_ratings > 0 else
        ft.Text("Aún no hay calificaciones de equipos registradas.", size=12.5, color=theme.TEXT_MUTED)
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Rendimiento de equipos", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Promedio mensual de calificaciones (últimos 6 meses).",
                        size=12, color=theme.TEXT_SECONDARY),
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
