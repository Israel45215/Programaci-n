import datetime
import flet as ft
import theme
from dao.task_dao import delete_task, get_all_tasks_with_details, init_db, insert_task, update_task
from dao.pseudo_project_dao import get_all_pseudo_projects, init_pseudo_projects_db
from dao.team_dao import get_all_teams, init_teams_db


class TasksView:
    def __init__(self, page: ft.Page):
        self.page = page
        init_db()
        init_pseudo_projects_db()
        init_teams_db()
        self.tasks = get_all_tasks_with_details()
        self.filter_selected = "Todas"

        self.summary_row_container = ft.Container()
        self.tasks_list_container = ft.Container()

    def refresh_ui(self):
        self.tasks = get_all_tasks_with_details()
        self.summary_row_container.content = self._build_summary_row()
        self.tasks_list_container.content = self._build_tasks_list()
        self.page.update()

    def _pseudo_project_options(self):
        pseudos = get_all_pseudo_projects()
        teams = {t["id"]: t["name"] for t in get_all_teams()}
        options = [ft.dropdown.Option(key="none", text="Sin asignar")]
        for pp in pseudos:
            team_label = teams.get(pp.get("team_id"), "Sin equipo")
            options.append(ft.dropdown.Option(key=str(pp["id"]), text=f'{pp["name"]} ({team_label})'))
        return options

    def _get_status_badge(self, status: str) -> ft.Container:
        color_map = {
            "Completada": (theme.GREEN, "#102A1D"),
            "En Proceso": (theme.BLUE, "#141F48"),
            "Pendiente": ("#F59E0B", "#2D220E"),
        }
        text_color, bg_color = color_map.get(status, (theme.TEXT_SECONDARY, theme.BG_CARD_ALT))

        return ft.Container(
            content=ft.Text(status, size=11, weight=ft.FontWeight.W_600, color=text_color),
            bgcolor=bg_color,
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
            border_radius=theme.RADIUS_PILL,
            alignment=ft.Alignment.CENTER,
        )

    def _get_priority_badge(self, priority: str) -> ft.Row:
        priority_colors = {
            "Alta": "#EF4444",
            "Media": "#F59E0B",
            "Baja": theme.GREEN,
        }
        color = priority_colors.get(priority, theme.TEXT_MUTED)

        return ft.Row(
            [
                ft.Container(width=7, height=7, border_radius=3.5, bgcolor=color),
                ft.Text(priority, size=12, color=theme.TEXT_SECONDARY),
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _stat_card(self, title: str, count: str, icon: str, icon_color: str) -> ft.Container:
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

    def _build_summary_row(self) -> ft.Row:
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
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("ID", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=30),
                    ft.Text("Tarea / Meta", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=175),
                    ft.Text("Responsable", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=115),
                    ft.Text("Prioridad", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=80),
                    ft.Text("Estado", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=95),
                    ft.Text("Progreso", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=105),
                    ft.Text("Inicio", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=85),
                    ft.Text("Límite", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, width=85),
                    ft.Container(
                        content=ft.Text("Acciones", size=11.5, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                        width=75,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border=ft.Border(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
        )

    def confirm_delete_task(self, task: dict):
        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def execute_delete(evt):
            delete_task(task["id"])
            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Eliminar Tarea", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content_padding=ft.Padding.only(left=24, right=24, top=16, bottom=16),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    [
                        ft.Text(f"¿Estás seguro de que deseas eliminar la tarea #{task['id']}:", size=13, color=theme.TEXT_SECONDARY),
                        ft.Text(f'"{task["title"]}"?', size=14, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text("Esta acción no se puede deshacer.", size=12, color="#EF4444"),
                    ],
                    tight=True,
                    spacing=8,
                ),
            ),
            actions_padding=ft.Padding.only(left=24, right=24, bottom=20, top=10),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(
                            content=ft.Text("Cancelar", size=13, color=theme.TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                            on_click=close_dialog,
                        ),
                        ft.ElevatedButton(
                            content=ft.Text("Eliminar", size=13, color="#FFFFFF", weight=ft.FontWeight.W_600),
                            bgcolor="#EF4444",
                            on_click=execute_delete,
                        ),
                    ],
                    spacing=12,
                )
            ],
        )

        if hasattr(self.page, "open"):
            self.page.open(dialog)
        else:
            self.page.dialog = dialog
            dialog.open = True
            if dialog not in self.page.overlay:
                self.page.overlay.append(dialog)
            self.page.update()

    def open_edit_modal(self, task: dict):
        today_str = datetime.date.today().strftime("%Y-%m-%d")

        def create_label(text: str, is_required: bool = False) -> ft.Row:
            controls = [ft.Text(text, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY)]
            if is_required:
                controls.append(ft.Text("*", size=13, weight=ft.FontWeight.BOLD, color="#EF4444"))
            return ft.Row(controls, spacing=2)

        txt_title = ft.TextField(
            value=task["title"],
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_pseudo = ft.Dropdown(
            options=self._pseudo_project_options(),
            value=str(task["pseudo_project_id"]) if task.get("pseudo_project_id") else "none",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        txt_assigned = ft.TextField(
            value=task["assigned"],
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_priority = ft.Dropdown(
            options=[
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Baja"),
            ],
            value=task["priority"],
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        initial_start = task.get("start_date")
        if not initial_start or initial_start == "-":
            initial_start = today_str

        txt_start_date = ft.TextField(
            value=initial_start,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            suffix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        txt_limit_date = ft.TextField(
            value=task["date"],
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            suffix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_status = ft.Dropdown(
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("En Proceso"),
                ft.dropdown.Option("Completada"),
            ],
            value=task["status"] if task["status"] in ["Pendiente", "En Proceso", "Completada"] else "En Proceso",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        initial_pct = int(round((task.get("progress") or 0.0) * 100))

        progress_label = ft.Text(f"Progreso: {initial_pct}%", size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY)

        sl_progress = ft.Slider(
            min=0,
            max=100,
            divisions=20,
            value=initial_pct,
            label="{value}%",
            active_color=theme.INDIGO,
        )

        def on_progress_change(e):
            progress_label.value = f"Progreso: {int(sl_progress.value)}%"
            progress_label.update()

        sl_progress.on_change = on_progress_change

        general_error = ft.Text("", size=12, color="#EF4444", visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_changes(evt):
            if not txt_title.value or not txt_limit_date.value:
                general_error.value = "Por favor, completa los campos requeridos (*)."
                general_error.visible = True
                general_error.update()
                return

            new_progress = sl_progress.value / 100

            pseudo_id = None if dd_pseudo.value == "none" else int(dd_pseudo.value)

            update_task(
                task_id=task["id"],
                title=txt_title.value,
                pseudo_project_id=pseudo_id,
                assigned=txt_assigned.value or "Sin Asignar",
                priority=dd_priority.value,
                status=dd_status.value,
                progress=new_progress,
                start_date=txt_start_date.value or today_str,
                date=txt_limit_date.value,
            )

            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text(f"Editar Tarea #{task['id']}", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content_padding=ft.Padding.only(left=24, right=24, top=16, bottom=16),
            content=ft.Container(
                width=450,
                height=560,
                content=ft.Column(
                    [
                        ft.Column([create_label("Título de la tarea", is_required=True), txt_title], spacing=6),
                        ft.Column([create_label("Meta"), dd_pseudo], spacing=6),
                        ft.Column([create_label("Responsable", is_required=True), txt_assigned], spacing=6),
                        ft.Row(
                            [
                                ft.Column([create_label("Prioridad"), dd_priority], spacing=6, expand=True),
                                ft.Column([create_label("Estado"), dd_status], spacing=6, expand=True),
                            ],
                            spacing=14,
                        ),
                        ft.Column([progress_label, sl_progress], spacing=2),
                        ft.Column([create_label("Fecha de inicio", is_required=True), txt_start_date], spacing=6),
                        ft.Column([create_label("Fecha límite", is_required=True), txt_limit_date], spacing=6),
                        general_error,
                    ],
                    tight=True,
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions_padding=ft.Padding.only(left=24, right=24, bottom=20, top=10),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(
                            content=ft.Text("Cancelar", size=13, color=theme.TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                            on_click=close_dialog,
                        ),
                        ft.ElevatedButton(
                            content=ft.Text("Guardar cambios", size=13, color="#FFFFFF", weight=ft.FontWeight.W_600),
                            bgcolor=theme.INDIGO,
                            on_click=save_changes,
                        ),
                    ],
                    spacing=12,
                )
            ],
        )

        if hasattr(self.page, "open"):
            self.page.open(dialog)
        else:
            self.page.dialog = dialog
            dialog.open = True
            if dialog not in self.page.overlay:
                self.page.overlay.append(dialog)
            self.page.update()

    def open_add_modal(self, e):
        today_str = datetime.date.today().strftime("%Y-%m-%d")

        def create_label(text: str, is_required: bool = False) -> ft.Row:
            controls = [ft.Text(text, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY)]
            if is_required:
                controls.append(ft.Text("*", size=13, weight=ft.FontWeight.BOLD, color="#EF4444"))
            return ft.Row(controls, spacing=2)

        txt_title = ft.TextField(
            hint_text="Ej: Diseñar página de inicio",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_pseudo = ft.Dropdown(
            options=self._pseudo_project_options(),
            value="none",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        txt_assigned = ft.TextField(
            value="",
            hint_text="Ej: Rubén",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_priority = ft.Dropdown(
            options=[
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Baja"),
            ],
            value="Media",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        txt_start_date = ft.TextField(
            value=today_str,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            suffix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        txt_limit_date = ft.TextField(
            hint_text="AAAA-MM-DD",
            value=today_str,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            suffix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
        )

        dd_status = ft.Dropdown(
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("En Proceso"),
            ],
            value="En Proceso",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.INDIGO,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        progress_label = ft.Text("Progreso: 0%", size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY)

        sl_progress = ft.Slider(
            min=0,
            max=100,
            divisions=20,
            value=0,
            label="{value}%",
            active_color=theme.INDIGO,
        )

        def on_progress_change(e):
            progress_label.value = f"Progreso: {int(sl_progress.value)}%"
            progress_label.update()

        sl_progress.on_change = on_progress_change

        general_error = ft.Text("", size=12, color="#EF4444", visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_task(evt):
            if not txt_title.value or not txt_limit_date.value:
                general_error.value = "Por favor, completa los campos requeridos (*)."
                general_error.visible = True
                general_error.update()
                return

            initial_status = dd_status.value
            initial_progress = sl_progress.value / 100

            pseudo_id = None if dd_pseudo.value == "none" else int(dd_pseudo.value)

            insert_task(
                title=txt_title.value,
                pseudo_project_id=pseudo_id,
                assigned=txt_assigned.value or "Sin Asignar",
                priority=dd_priority.value,
                status=initial_status,
                progress=initial_progress,
                start_date=txt_start_date.value or today_str,
                date=txt_limit_date.value,
            )

            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Agregar nueva tarea", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content_padding=ft.Padding.only(left=24, right=24, top=16, bottom=16),
            content=ft.Container(
                width=450,
                content=ft.Column(
                    [
                        ft.Column([create_label("Título de la tarea", is_required=True), txt_title], spacing=6),
                        ft.Column([create_label("Meta"), dd_pseudo], spacing=6),
                        ft.Column([create_label("Responsable", is_required=True), txt_assigned], spacing=6),
                        ft.Row(
                            [
                                ft.Column([create_label("Prioridad"), dd_priority], spacing=6, expand=True),
                                ft.Column([create_label("Estado inicial"), dd_status], spacing=6, expand=True),
                            ],
                            spacing=14,
                        ),
                        ft.Column([progress_label, sl_progress], spacing=2),
                        ft.Column([create_label("Fecha de inicio", is_required=True), txt_start_date], spacing=6),
                        ft.Column([create_label("Fecha límite", is_required=True), txt_limit_date], spacing=6),
                        general_error,
                    ],
                    tight=True,
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions_padding=ft.Padding.only(left=24, right=24, bottom=20, top=10),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(
                            content=ft.Text("Cancelar", size=13, color=theme.TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                            on_click=close_dialog,
                        ),
                        ft.ElevatedButton(
                            content=ft.Text("Crear tarea", size=13, color="#FFFFFF", weight=ft.FontWeight.W_600),
                            bgcolor=theme.INDIGO,
                            on_click=save_task,
                        ),
                    ],
                    spacing=12,
                )
            ],
        )

        if hasattr(self.page, "open"):
            self.page.open(dialog)
        else:
            self.page.dialog = dialog
            dialog.open = True
            if dialog not in self.page.overlay:
                self.page.overlay.append(dialog)
            self.page.update()

    def _task_row(self, task: dict) -> ft.Container:
        pct = int(task.get("progress", 0) * 100)

        progress_bar = ft.Column(
            [
                ft.Row(
                    [ft.Text(f"{pct}%", size=10.5, color=theme.TEXT_MUTED, weight=ft.FontWeight.W_600)],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.ProgressBar(
                    value=task.get("progress", 0),
                    color=theme.CYAN if pct < 100 else theme.GREEN,
                    bgcolor=theme.BG_INPUT,
                    height=5,
                ),
            ],
            spacing=1,
            width=105,
        )

        start_dt_val = task.get("start_date") or "-"
        limit_dt_val = task.get("date") or "-"

        pseudo_label = task.get("pseudo_project_name") or "Sin asignar"
        team_label = task.get("team_name")
        subtitle = f"{pseudo_label} · {team_label}" if team_label else pseudo_label

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(f"#{task['id']}", size=11.5, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED, width=30),
                    ft.Column(
                        [
                            ft.Text(task["title"], size=12.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                            ft.Text(subtitle, size=10.5, color=theme.TEXT_MUTED),
                        ],
                        spacing=1,
                        width=175,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON, size=11, color="#FFFFFF"),
                                width=20,
                                height=20,
                                border_radius=10,
                                bgcolor=theme.INDIGO,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Text(task["assigned"], size=12, color=theme.TEXT_SECONDARY),
                        ],
                        spacing=6,
                        width=115,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(content=self._get_priority_badge(task["priority"]), width=80),
                    ft.Container(content=self._get_status_badge(task["status"]), width=95),
                    ft.Container(content=progress_bar, width=105),
                    ft.Text(start_dt_val, size=11.5, color=theme.TEXT_MUTED, width=85),
                    ft.Text(limit_dt_val, size=11.5, color=theme.TEXT_MUTED, width=85),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=theme.TEXT_MUTED,
                                    icon_size=15,
                                    tooltip="Editar",
                                    on_click=lambda e, t=task: self.open_edit_modal(t),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color="#EF4444",
                                    icon_size=15,
                                    tooltip="Eliminar",
                                    on_click=lambda e, t=task: self.confirm_delete_task(t),
                                ),
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=75,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD_ALT,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=10,
        )

    def _build_tasks_list(self) -> ft.Column:
        filtered_tasks = [
            t for t in self.tasks if self.filter_selected == "Todas" or t["status"] == self.filter_selected
        ]
        return ft.Column(
            [
                self._build_table_header(),
                ft.Container(height=6),
                *[self._task_row(t) for t in filtered_tasks],
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

    def build(self) -> ft.Container:
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
                    on_click=self.open_add_modal,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        def change_filter(status: str):
            self.filter_selected = status
            self.refresh_ui()

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
                    on_click=lambda e, s=status: change_filter(s),
                    ink=True,
                )
            )

        filters_bar = ft.Row(filter_buttons, spacing=6)

        self.summary_row_container.content = self._build_summary_row()
        self.tasks_list_container.content = self._build_tasks_list()

        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Container(height=16),
                    self.summary_row_container,
                    ft.Container(height=20),
                    filters_bar,
                    ft.Container(height=10),
                    ft.Container(
                        content=self.tasks_list_container,
                        bgcolor=theme.BG_CARD,
                        border_radius=theme.RADIUS_CARD,
                        padding=theme.PADDING_CARD,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )