import flet as ft
import theme
from ui.components.calendar_view import CalendarView
from ui.components.topbar import Topbar
from ui.components.sidebar import Sidebar
from ui.components.dashboard_view import build_dashboard_view
from ui.components.projects_view import ProjectsView
from ui.components.tasks_view import TasksView
from ui.components.teams_view import TeamsView
from ui.components.employees_view import EmployeesView
from ui.components.footer import build_footer
from ui.components.performance_view import build_performance_view


class MainWindow(ft.Container):
    def __init__(self, page: ft.Page, on_logout=None):
        super().__init__()
        self.page_ref = page
        self.on_logout = on_logout
        self.expand = True
        self.bgcolor = theme.BG_MAIN

        # Barra superior
        self.topbar = Topbar(self.page_ref)

        # Contenedor principal del contenido (aquí se intercambian las vistas)
        self.content_area = ft.Container(
            content=build_dashboard_view(),
            expand=True,
        )

        # Función para manejar el cambio de vistas desde el sidebar
        def handle_change_view(name):
            if name == "dashboard":
                self.content_area.content = build_dashboard_view()
            elif name == "projects":
                self.content_area.content = ProjectsView(self.page_ref).build()
            elif name == "tasks":
                self.content_area.content = TasksView(self.page_ref).build()
            elif name == "workers":
                self.content_area.content = TeamsView(self.page_ref).build()
            elif name == "employees":
                self.content_area.content = EmployeesView(self.page_ref).build()
            elif name == "performance":
                self.content_area.content = build_performance_view(self.page_ref)
            elif name == "calendar":
                self.content_area.content = CalendarView(self.page_ref).build()
            else:
                self.content_area.content = ft.Container(
                    content=ft.Text(
                        f"Vista '{name}' en construcción",
                        color=theme.TEXT_SECONDARY,
                        size=16,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                )
            self.content_area.update()

        # Barra lateral izquierda pasando page y la función de cambio de vista
        self.sidebar = Sidebar(
            self.page_ref,
            handle_change_view,
            on_logout=self.on_logout,
        )

        # Área derecha que agrupa la barra superior y la vista actual
        self.right_panel = ft.Column(
            [
                self.topbar,
                self.content_area,
            ],
            spacing=0,
            expand=True,
        )

        # Fila principal: Sidebar a la izquierda, Panel derecho al resto
        self.main_row = ft.Row(
            [
                self.sidebar,
                self.right_panel,
            ],
            spacing=0,
            expand=True,
        )

        # Footer fijo abajo, ocupando todo el ancho
        self.footer = build_footer(self.page_ref)

        # Estructura general de la ventana
        self.content = ft.Column(
            [
                self.main_row,
                self.footer,
            ],
            spacing=0,
            expand=True,
        )