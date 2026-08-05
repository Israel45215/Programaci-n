import flet as ft
import theme

class Sidebar(ft.Container):
    def __init__(self, page: ft.Page, on_change_view, on_logout=None):
        super().__init__()
        self.page_ref = page
        self.on_change_view = on_change_view
        self.on_logout = on_logout
        self.width = 260
        self.bgcolor = theme.BG_SIDEBAR
        self.padding = 16
        
        self.current_selected = "dashboard"
        self.content = self._build_sidebar_content()

    def _build_nav_item(self, name, label, icon, badge_count=None):
        is_selected = self.current_selected == name
        
        row_controls = [
            ft.Icon(
                icon, 
                color=theme.ACCENT_COLOR if is_selected else theme.TEXT_SECONDARY, 
                size=20
            ),
            ft.Text(
                label,
                color=theme.TEXT_PRIMARY if is_selected else theme.TEXT_SECONDARY,
                weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL,
                size=14,
            ),
        ]
        
        if badge_count:
            row_controls.append(ft.Container(expand=True))
            row_controls.append(
                ft.Container(
                    content=ft.Text(str(badge_count), size=11, color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.RED_600,
                    border_radius=10,
                    padding=6,
                )
            )

        return ft.Container(
            on_click=lambda e: self.select_view(name),
            bgcolor=theme.SIDEBAR_ACTIVE_BG if is_selected else ft.Colors.TRANSPARENT,
            border_radius=8,
            padding=10,
            content=ft.Row(row_controls, spacing=12),
        )

    def select_view(self, name):
        self.current_selected = name
        self.content = self._build_sidebar_content()
        self.update()
        self.on_change_view(name)

    def _build_sidebar_content(self):
        return ft.Column(
            [
                # Logo y Título superior
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        [
                            ft.Container(
                                width=32,
                                height=32,
                                bgcolor=theme.ACCENT_COLOR,
                                border_radius=8,
                                content=ft.Icon(ft.Icons.CODE, color=theme.TEXT_PRIMARY, size=18)
                            ),
                            ft.Text(
                                "DevTrack",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=theme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=10,
                    ),
                ),
                
                ft.Container(height=5),

                ft.Text("GENERAL", size=11, weight=ft.FontWeight.BOLD, color=theme.TEXT_SECONDARY),
                ft.Container(height=5),

                # Opciones principales
                self._build_nav_item("dashboard", "Dashboard", ft.Icons.GRID_VIEW),
                self._build_nav_item("projects", "Proyectos", ft.Icons.FOLDER),
                self._build_nav_item("employees", "Empleados", ft.Icons.BADGE_ROUNDED),
                
                ft.Container(height=10),
                ft.Text("REPORTES", size=11, weight=ft.FontWeight.BOLD, color=theme.TEXT_SECONDARY),
                ft.Container(height=5),
                
                self._build_nav_item("tasks", "Tareas", ft.Icons.CHECK_CIRCLE),
                self._build_nav_item("workers", "Equipos", ft.Icons.GROUP),
                self._build_nav_item("performance", "Rendimiento", ft.Icons.AUTO_GRAPH),
                
                ft.Container(height=10),
                ft.Text("AGENDA", size=11, weight=ft.FontWeight.BOLD, color=theme.TEXT_SECONDARY),
                ft.Container(height=5),
                
                self._build_nav_item("calendar", "Calendario", ft.Icons.CALENDAR_MONTH),

                ft.Container(expand=True),
                
                # Botón inferior de cerrar sesión
                ft.Container(
                    on_click=lambda e: self.on_logout() if self.on_logout else None,
                    padding=10,
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGOUT, color=theme.TEXT_SECONDARY, size=20),
                        ],
                        spacing=12,
                    ),
                ),
            ],
            expand=True,
            spacing=4,
        )