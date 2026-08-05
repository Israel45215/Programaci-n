import flet as ft
import theme

from ui.components.metric_card import build_metric_card
from ui.components.mini_calendar import build_mini_calendar
from ui.components.recent_activity import (
    build_recent_teams_card,
    build_finished_projects_chart,
)
from ui.components.dashboard_extras import (
    build_new_projects_table,
    build_project_deadlines_calendar,
    build_team_performance_chart,
)
from dao.project_dao import get_all_projects
from dao.task_dao import get_all_tasks


def _section_header() -> ft.Row:
    return ft.Row(
        [
            ft.Text(
                "Dashboard",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme.TEXT_PRIMARY,
            ),
        ]
    )


def _summary_toolbar() -> ft.Row:
    return ft.Row(
        [
            ft.Container(
                content=ft.Text(
                    "Resumen general",
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color=theme.TEXT_PRIMARY,
                ),
                bgcolor=theme.BG_SIDEBAR,
                padding=12,
                border_radius=20,
            ),
            ft.Container(expand=True),
            ft.Icon(
                ft.Icons.MORE_HORIZ_ROUNDED,
                size=20,
                color=theme.TEXT_SECONDARY,
            ),
        ]
    )


def build_dashboard_view() -> ft.Container:
    projects = get_all_projects()
    tasks = get_all_tasks()

    active_projects = sum(
        1 for project in projects
        if project.get("status") == "Activo"
    )

    total_tasks = len(tasks)

    pending_tasks = sum(
        1 for task in tasks
        if task["status"] == "Pendiente"
    )

    completed_tasks = sum(
        1 for task in tasks
        if task["status"] == "Completada"
    )

    avg_progress = (
        sum(task.get("progress") or 0.0 for task in tasks) / total_tasks
        if total_tasks
        else 0.0
    )

    metrics_row = ft.Row(
        [
            build_metric_card(
                "Proyectos",
                "Activos",
                active_projects / len(projects) if projects else 0.0,
                theme.GREEN,
                str(active_projects),
                (
                    f"de {len(projects)} proyectos registrados"
                    if projects
                    else "Sin proyectos aún"
                ),
            ),
            build_metric_card(
                "Tareas pendientes",
                "Por iniciar",
                pending_tasks / total_tasks if total_tasks else 0.0,
                theme.ERROR_COLOR,
                str(pending_tasks),
                (
                    f"de {total_tasks} tareas registradas"
                    if total_tasks
                    else "Sin tareas aún"
                ),
            ),
            build_metric_card(
                "Tareas completadas",
                "Total",
                completed_tasks / total_tasks if total_tasks else 0.0,
                theme.CYAN,
                str(completed_tasks),
                (
                    f"de {total_tasks} tareas registradas"
                    if total_tasks
                    else "Sin tareas aún"
                ),
            ),
            build_metric_card(
                "Productividad",
                "Promedio general",
                avg_progress,
                theme.PURPLE,
                f"{avg_progress * 100:.0f}%",
                (
                    "Con base en el avance de todas las tareas"
                    if total_tasks
                    else "Sin datos aún"
                ),
            ),
        ],
        spacing=16,
    )

    # Calendario mensual compacto, centrado y con cuadrícula.
    calendar_row = ft.Row(
        [
            ft.Container(
                content=build_mini_calendar(),
                width=520,
                height=390,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Tabla de proyectos nuevos + calendario de fechas límite.
    projects_row = ft.Row(
        [
            build_new_projects_table(),
            build_project_deadlines_calendar(),
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        height=340,
    )

    # Equipos recientes + gráficas inferiores.
    activity_row = ft.Row(
        [
            build_recent_teams_card(),
            build_finished_projects_chart(),
            build_team_performance_chart(),
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        height=260,
    )

    return ft.Container(
        content=ft.Column(
            [
                _section_header(),
                ft.Container(height=14),
                _summary_toolbar(),
                ft.Container(height=16),
                metrics_row,
                ft.Container(height=22),
                calendar_row,
                ft.Container(height=22),
                projects_row,
                ft.Container(height=16),
                activity_row,
                ft.Container(height=24),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )