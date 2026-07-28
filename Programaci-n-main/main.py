import flet as ft
import theme

from components.sidebar import build_sidebar
from components.topbar import build_topbar
from components.dashboard_view import build_dashboard_view
from components.projects_view import ProjectsView
from components.tasks_view import TasksView


def _placeholder_view(route_name: str) -> ft.Container:
    """Vista temporal para rutas que todavía no se han maquetado/construido."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.CONSTRUCTION_ROUNDED, size=42, color=theme.TEXT_MUTED),
                ft.Text(f"Vista '{route_name}' próximamente", size=16, color=theme.TEXT_SECONDARY),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )


def main(page: ft.Page):
    page.title = "DevTrack - Panel del Administrador"
    page.bgcolor = theme.BG_PAGE
    page.padding = 0
    page.window.width = 1400
    page.window.height = 860
    page.window.min_width = 1100
    page.window.min_height = 700
    page.fonts = {}
    page.theme_mode = ft.ThemeMode.DARK

    # Estado global del panel con la vista de tareas agregada
    state = {
        "route": "dashboard", 
        "projects_view": None,
        "tasks_view": None
    }

    content_area = ft.Container(expand=True)

    def render_route():
        route = state["route"]
        if route == "dashboard":
            content_area.content = build_dashboard_view()
        elif route == "proyectos":
            if state["projects_view"] is None:
                state["projects_view"] = ProjectsView(page)
            content_area.content = state["projects_view"].build()
        elif route == "tareas":
            if state["tasks_view"] is None:
                state["tasks_view"] = TasksView(page)
            content_area.content = state["tasks_view"].build()
        elif route == "logout":
            content_area.content = _placeholder_view("Cerrar sesión")
        else:
            content_area.content = _placeholder_view(route)
        page.update()

    def on_navigate(route: str):
        state["route"] = route
        sidebar.content = build_sidebar(state["route"], on_navigate).content
        render_route()

    sidebar = build_sidebar(state["route"], on_navigate)

    layout = ft.Row(
        [
            sidebar,
            ft.Column(
                [
                    build_topbar(),
                    content_area,
                ],
                expand=True,
                spacing=0,
            ),
        ],
        spacing=0,
        expand=True,
    )

    page.add(layout)
    render_route()


if __name__ == "__main__":
    ft.run(main)