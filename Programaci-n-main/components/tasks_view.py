import flet as ft
import theme

# Datos de prueba pertenecientes únicamente a DevTrack
TASKS_DATA = [
    {
        "id": 1,
        "title": "Diseñar arquitectura del módulo",
        "project": "DevTrack",
        "assigned": "Rubén",
        "priority": "Alta",
        "status": "En Proceso",
        "progress": 0.65,  # 65%
        "date": "2026-07-28",
    },
    {
        "id": 2,
        "title": "Implementar autenticación JWT",
        "project": "DevTrack",
        "assigned": "Ana",
        "priority": "Media",
        "status": "Pendiente",
        "progress": 0.10,  # 10%
        "date": "2026-07-30",
    },
    {
        "id": 3,
        "title": "Optimizar consultas SQL",
        "project": "DevTrack",
        "assigned": "Doreen",
        "priority": "Baja",
        "status": "Completada",
        "progress": 1.0,  # 100%
        "date": "2026-07-25",
    },
]


class TasksView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tasks = TASKS_DATA.copy()
        self.filter_selected = "Todas"

    def _get_status_badge(self, status: str) -> ft.Container:
        """Badge visual con color según el estado."""
        color_map = {
            "Completada": (theme.GREEN, "#102A1D"),
            "En Proceso": (theme.BLUE, "#141F48"),
            "Pendiente": ("#F59E0B", "#2D220E"),
        }
        text_color, bg_color = color_map.get(status, (theme.TEXT_SECONDARY, theme.BG_CARD_ALT))

        return ft.Container(
            content=ft.Text(status, size=11.5, weight=ft.FontWeight.W_600, color=text_color),
            bgcolor=bg_color,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=theme.RADIUS_PILL,
        )

    def _get_priority_badge(self, priority: str) -> ft.Container:
        """Indicador con punto de color según la prioridad."""
        priority_colors = {
            "Alta": "#EF4444",
            "Media": "#F59E0B",
            "Baja": theme.GREEN,
        }
        color = priority_colors.get(priority, theme.TEXT_MUTED)

        return ft.Row(
            [
                ft.Container(width=8, height=8, border_radius=4, bgcolor=color),
                ft.Text(priority, size=12.5, color=theme.TEXT_SECONDARY),
            ],
            spacing=6,
        )

    def _stat_card(self, title: str, count: str, icon: str, icon_color: str) -> ft.Container:
        """Tarjeta superior de resumen estadístico."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=22, color=icon_color),
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=theme.BG_INPUT,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(title, size=12, color=theme.TEXT_SECONDARY),
                            ft.Text(count, size=20, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=14,
            ),
            bgcolor=theme.BG_CARD,
            padding=16,
            border_radius=theme.RADIUS_CARD,
            expand=True,
        )

    def _build_summary_row(self):
        """Fila superior con contadores de tareas."""
        total = len(self.tasks)
        pending = sum(1 for t in self.tasks if t["status"] == "Pendiente")
        in_progress = sum(1 for t in self.tasks if t["status"] == "En Proceso")
        done = sum(1 for t in self.tasks if t["status"] == "Completada")

        return ft.Row(
            [
                self._stat_card("Total Tareas", str(total), ft.Icons.TASK_ALT_ROUNDED, theme.CYAN),
                self._stat_card("Pendientes", str(pending), ft.Icons.PENDING_ACTIONS_ROUNDED, "#F59E0B"),
                self._stat_card("En Proceso", str(in_progress), ft.Icons.AUTORENEW_ROUNDED, theme.BLUE),
                self._stat_card("Completadas", str(done), ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, theme.GREEN),
            ],
            spacing=16,
        )

    def _build_table_header(self) -> ft.Container:
        """Fila de encabezado indicando el nombre de cada columna."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("ID", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=40),
                    ft.Text("Tarea / Proyecto", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=220),
                    ft.Text("Responsable", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=130),
                    ft.Text("Prioridad", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=100),
                    ft.Text("Estado", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=110),
                    ft.Text("Progreso", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=130),
                    ft.Text("Fecha Límite", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=100),
                    ft.Container(expand=True),
                    ft.Text("Acciones", size=12, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=70, text_align=ft.TextAlign.RIGHT),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border=ft.Border(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
        )

    def _task_row(self, task: dict) -> ft.Container:
        """Fila individual de la tarea con todos sus campos y barra de progreso."""
        pct = int(task.get("progress", 0) * 100)

        progress_bar = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"{pct}%", size=11, color=theme.TEXT_MUTED, weight=ft.FontWeight.W_600),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.ProgressBar(
                    value=task.get("progress", 0),
                    color=theme.CYAN if pct < 100 else theme.GREEN,
                    bgcolor=theme.BG_INPUT,
                    height=6,
                ),
            ],
            spacing=2,
            width=110,
        )

        return ft.Container(
            content=ft.Row(
                [
                    # ID
                    ft.Text(f"#{task['id']}", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED, width=40),
                    
                    # Título y Proyecto
                    ft.Column(
                        [
                            ft.Text(task["title"], size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                            ft.Text(task["project"], size=11, color=theme.TEXT_MUTED),
                        ],
                        spacing=2,
                        width=220,
                    ),
                    
                    # Responsable
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON, size=12, color="#FFFFFF"),
                                width=22,
                                height=22,
                                border_radius=11,
                                bgcolor=theme.INDIGO,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Text(task["assigned"], size=12.5, color=theme.TEXT_SECONDARY),
                        ],
                        spacing=8,
                        width=130,
                    ),
                    
                    # Prioridad
                    ft.Container(content=self._get_priority_badge(task["priority"]), width=100),
                    
                    # Estado
                    ft.Container(content=self._get_status_badge(task["status"]), width=110),
                    
                    # Barra de Progreso
                    ft.Container(content=progress_bar, width=130),
                    
                    # Fecha Límite
                    ft.Text(task["date"], size=12, color=theme.TEXT_MUTED, width=100),
                    
                    ft.Container(expand=True),
                    
                    # Acciones
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=theme.TEXT_MUTED,
                                icon_size=16,
                                tooltip="Editar",
                                on_click=lambda e: None,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color="#EF4444",
                                icon_size=16,
                                tooltip="Eliminar",
                                on_click=lambda e: None,
                            ),
                        ],
                        spacing=0,
                        width=70,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD_ALT,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=10,
        )

    def open_add_modal(self, e):
        """Modal para registrar nueva tarea en DevTrack."""
        txt_title = ft.TextField(
            label="Título de la tarea",
            border_color=theme.BORDER_SOFT,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY),
        )
        txt_assigned = ft.TextField(
            label="Responsable",
            value="Rubén",
            border_color=theme.BORDER_SOFT,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY),
        )
        dd_priority = ft.Dropdown(
            label="Prioridad",
            options=[
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Baja"),
            ],
            value="Media",
            border_color=theme.BORDER_SOFT,
        )

        def close_dialog(e):
            self.page.close(dialog)

        def save_task(e):
            if txt_title.value:
                self.tasks.append(
                    {
                        "id": len(self.tasks) + 1,
                        "title": txt_title.value,
                        "project": "DevTrack",
                        "assigned": txt_assigned.value or "Sin Asignar",
                        "priority": dd_priority.value,
                        "status": "Pendiente",
                        "progress": 0.0,
                        "date": "2026-07-28",
                    }
                )
                self.page.close(dialog)
                self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Crear Nueva Tarea", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            bgcolor=theme.BG_CARD,
            content=ft.Column(
                [
                    txt_title,
                    txt_assigned,
                    dd_priority,
                ],
                tight=True,
                spacing=12,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton("Guardar", bgcolor=theme.INDIGO, color="#FFFFFF", on_click=save_task),
            ],
        )

        self.page.open(dialog)

    def build(self) -> ft.Container:
        """Construye la vista principal de Tareas."""
        header = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Gestión de Tareas", size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text("Administra, asigna y monitorea el avance del equipo", size=13, color=theme.TEXT_SECONDARY),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ADD_ROUNDED, size=18, color="#FFFFFF"),
                            ft.Text("Nueva Tarea", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                        ],
                        spacing=6,
                    ),
                    bgcolor=theme.INDIGO,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                    ),
                    on_click=self.open_add_modal,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        filter_buttons = []
        for status in ["Todas", "Pendiente", "En Proceso", "Completada"]:
            is_active = self.filter_selected == status
            filter_buttons.append(
                ft.Container(
                    content=ft.Text(
                        status,
                        size=12.5,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
                        color=theme.TEXT_PRIMARY if is_active else theme.TEXT_SECONDARY,
                    ),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    border_radius=theme.RADIUS_PILL,
                    bgcolor=theme.SIDEBAR_ACTIVE_BG if is_active else "transparent",
                    on_click=lambda e, s=status: None,
                    ink=True,
                )
            )

        filters_bar = ft.Row(filter_buttons, spacing=6)

        filtered_tasks = [
            t for t in self.tasks if self.filter_selected == "Todas" or t["status"] == self.filter_selected
        ]

        tasks_list = ft.Column(
            [
                self._build_table_header(),
                ft.Container(height=6),
                *[self._task_row(t) for t in filtered_tasks],
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        content = ft.Column(
            [
                header,
                ft.Container(height=16),
                self._build_summary_row(),
                ft.Container(height=20),
                filters_bar,
                ft.Container(height=10),
                ft.Container(
                    content=tasks_list,
                    bgcolor=theme.BG_CARD,
                    border_radius=theme.RADIUS_CARD,
                    padding=theme.PADDING_CARD,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        return ft.Container(
            content=content,
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )