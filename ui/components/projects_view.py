import flet as ft
import theme
from dao.project_dao import (
    get_all_projects, insert_project, init_projects_db,
    update_project, delete_project,
)
from dao.pseudo_project_dao import (
    get_pseudo_projects_by_project, insert_pseudo_project,
    update_pseudo_project, delete_pseudo_project, init_pseudo_projects_db,
)
from dao.team_dao import get_all_teams, init_teams_db

TECH_OPTIONS = ["React", "Vue", "Angular", "Svelte", "HTML/CSS", "TypeScript", "Tailwind CSS", "Next.js"]


class ProjectsView:
    def __init__(self, page: ft.Page):
        self.page = page
        init_projects_db()
        init_pseudo_projects_db()
        init_teams_db()
        self.projects = get_all_projects()
        self.projects_container = ft.Container()

    def refresh_ui(self):
        self.projects = get_all_projects()
        self.projects_container.content = self._build_projects_grid()
        self.page.update()

    def _pseudo_count(self, project_id) -> int:
        return len(get_pseudo_projects_by_project(project_id))

    def _team_name(self, team_id) -> str:
        if not team_id:
            return "Sin equipo asignado"
        teams = get_all_teams()
        for t in teams:
            if t["id"] == team_id:
                return t["name"]
        return "Sin equipo asignado"

    # ---------- Tarjeta de proyecto ----------

    def _project_card(self, p: dict) -> ft.Container:
        pseudo_count = self._pseudo_count(p["id"])

        techs = [t for t in (p.get("technologies") or "").split(",") if t]
        tech_chips = ft.Row(
            [
                ft.Container(
                    content=ft.Text(t, size=10, color=theme.TEXT_PRIMARY),
                    bgcolor=theme.BG_INPUT,
                    border_radius=10,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                )
                for t in techs
            ],
            wrap=True,
            spacing=4,
        ) if techs else ft.Text("Sin tecnologías definidas", size=10, color=theme.TEXT_MUTED)

        return ft.Container(
            content=ft.Column([
                ft.Row(
                    [
                        ft.Text(p["name"], size=16, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=theme.TEXT_SECONDARY,
                            icon_size=16,
                            on_click=lambda e, proj=p: self.open_edit_modal(proj),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                            icon_color=theme.ERROR_COLOR,
                            icon_size=16,
                            on_click=lambda e, proj=p: self.confirm_delete_project(proj),
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(p.get("description") or "Sin descripción", size=13, color=theme.TEXT_SECONDARY),
                ft.Container(height=4),
                tech_chips,
                ft.Container(expand=True),
                ft.Row([
                    ft.Text(f"Estado: {p.get('status', 'Activo')}", size=11, color=theme.CYAN)
                ]),
                ft.Container(height=8),
                ft.OutlinedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LIST_ALT_ROUNDED, size=15, color=theme.ACCENT_COLOR),
                            ft.Text(f"Metas ({pseudo_count})", size=12, color=theme.TEXT_PRIMARY),
                        ],
                        spacing=6,
                    ),
                    on_click=lambda e, proj=p: self.open_pseudo_projects_modal(proj),
                ),
            ], spacing=6),
            bgcolor=theme.BG_CARD_ALT,
            padding=16,
            border_radius=12,
            width=280,
            height=230,
        )

    def _build_projects_grid(self):
        if not self.projects:
            return ft.Container(
                content=ft.Text("No hay proyectos registrados aún.", size=13, color=theme.TEXT_MUTED),
                padding=20
            )

        cards = [self._project_card(p) for p in self.projects]

        rows = []
        for i in range(0, len(cards), 3):
            row_cards = cards[i:i + 3]
            rows.append(ft.Row(row_cards, spacing=16))
        return ft.Column(rows, spacing=16)

    # ---------- Modal: formulario Proyecto ----------

    def open_create_modal(self):
        self._open_form_modal(project=None)

    def open_edit_modal(self, project: dict):
        self._open_form_modal(project=project)

    def _open_form_modal(self, project):
        is_edit = project is not None

        selected_techs = (project.get("technologies") or "").split(",") if is_edit else []
        selected_techs = [t for t in selected_techs if t]

        txt_name = ft.TextField(
            label="Nombre del proyecto",
            value=project["name"] if is_edit else "",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        txt_description = ft.TextField(
            label="Descripción del proyecto",
            value=project.get("description") if is_edit else "",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        dd_status = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Activo"),
                ft.dropdown.Option("Pausado"),
                ft.dropdown.Option("Finalizado"),
            ],
            value=project.get("status", "Activo") if is_edit else "Activo",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        tech_checkboxes = [
            ft.Checkbox(
                label=tech,
                value=tech in selected_techs,
                label_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
            )
            for tech in TECH_OPTIONS
        ]

        tech_section = ft.Column(
            [
                ft.Text("Tecnologías", size=12.5, color=theme.TEXT_SECONDARY),
                ft.Row(tech_checkboxes, wrap=True, spacing=10, run_spacing=4),
            ],
            spacing=6,
        )

        general_error = ft.Text("", size=12, color=theme.ERROR_COLOR, visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_project(evt):
            if not txt_name.value:
                general_error.value = "El nombre del proyecto es obligatorio."
                general_error.visible = True
                general_error.update()
                return

            techs_value = ",".join(cb.label for cb in tech_checkboxes if cb.value)

            if is_edit:
                update_project(project["id"], txt_name.value, txt_description.value, dd_status.value, techs_value)
            else:
                insert_project(txt_name.value, txt_description.value, dd_status.value, techs_value)

            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Editar Proyecto" if is_edit else "Nuevo Proyecto",
                            color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [txt_name, txt_description, dd_status, tech_section, general_error],
                    tight=True,
                    spacing=14,
                ),
            ),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(content=ft.Text("Cancelar", color=theme.TEXT_PRIMARY), on_click=close_dialog),
                        ft.ElevatedButton(
                            content=ft.Text("Guardar", color="#FFFFFF"),
                            bgcolor=theme.ACCENT_COLOR,
                            on_click=save_project,
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

    def confirm_delete_project(self, project: dict):
        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def execute_delete(evt):
            delete_project(project["id"])
            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Eliminar Proyecto", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=400,
                content=ft.Text(
                    f'¿Eliminar el proyecto "{project["name"]}"? Esto también afectará a sus metas. Esta acción no se puede deshacer.',
                    size=13, color=theme.TEXT_SECONDARY,
                ),
            ),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(content=ft.Text("Cancelar", color=theme.TEXT_PRIMARY), on_click=close_dialog),
                        ft.ElevatedButton(
                            content=ft.Text("Eliminar", color="#FFFFFF"),
                            bgcolor=theme.ERROR_COLOR,
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

    # ---------- Modal: lista de metas de un proyecto ----------

    def open_pseudo_projects_modal(self, project: dict):
        list_container = ft.Container()

        def build_list():
            pseudos = get_pseudo_projects_by_project(project["id"])
            if not pseudos:
                return ft.Container(
                    content=ft.Text("Este proyecto aún no tiene metas.", size=12.5, color=theme.TEXT_MUTED),
                    padding=16,
                )

            items = []
            for ps in pseudos:
                items.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(ps["name"], size=13.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                        ft.Text(ps.get("description") or "Sin descripción", size=12, color=theme.TEXT_SECONDARY),
                                        ft.Text(f'Equipo: {self._team_name(ps.get("team_id"))}', size=11.5, color=theme.CYAN),
                                        ft.Text(f'Estado: {ps.get("status", "Pendiente")}', size=11, color=theme.TEXT_MUTED),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=theme.TEXT_SECONDARY,
                                    icon_size=16,
                                    on_click=lambda e, pp=ps: self.open_pseudo_form_modal(project, pp),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color=theme.ERROR_COLOR,
                                    icon_size=16,
                                    on_click=lambda e, pp=ps: confirm_delete_pseudo(pp),
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        bgcolor=theme.BG_INPUT,
                        border_radius=8,
                        padding=12,
                        margin=ft.Margin.only(bottom=8),
                    )
                )
            return ft.Column(items, spacing=0, scroll=ft.ScrollMode.AUTO, height=280)

        def refresh_list():
            list_container.content = build_list()
            list_container.update()
            self.refresh_ui()

        def confirm_delete_pseudo(ps: dict):
            delete_pseudo_project(ps["id"])
            refresh_list()

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()
            self.refresh_ui()

        def open_new_pseudo(evt):
            self.open_pseudo_form_modal(project, None, on_saved=refresh_list)

        list_container.content = build_list()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f'Metas de "{project["name"]}"',
                                    color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=16),
                            ft.Text("Sub-proyectos asignados a equipos", size=11.5, color=theme.TEXT_SECONDARY),
                        ],
                        spacing=2,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=460,
                content=list_container,
            ),
            actions=[
                ft.Row(
                    [
                        ft.ElevatedButton(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.ADD, size=15, color="#FFFFFF"),
                                 ft.Text("Nuevo Meta", color="#FFFFFF", size=12.5)],
                                spacing=6,
                            ),
                            bgcolor=theme.ACCENT_COLOR,
                            on_click=open_new_pseudo,
                        ),
                        ft.Container(expand=True),
                        ft.OutlinedButton(content=ft.Text("Cerrar", color=theme.TEXT_PRIMARY), on_click=close_dialog),
                    ],
                )
            ],
        )

        # guardamos referencia para poder refrescar la lista tras crear uno nuevo
        self._active_pseudo_dialog_refresh = refresh_list

        if hasattr(self.page, "open"):
            self.page.open(dialog)
        else:
            self.page.dialog = dialog
            dialog.open = True
            if dialog not in self.page.overlay:
                self.page.overlay.append(dialog)
            self.page.update()

    # ---------- Modal: formulario Meta ----------

    def open_pseudo_form_modal(self, project: dict, pseudo: dict = None, on_saved=None):
        is_edit = pseudo is not None
        teams = get_all_teams()

        txt_name = ft.TextField(
            label="Nombre del meta",
            value=pseudo["name"] if is_edit else "",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        txt_description = ft.TextField(
            label="Descripción del meta",
            value=pseudo.get("description") if is_edit else "",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        team_options = [ft.dropdown.Option(key="none", text="Sin equipo asignado")]
        team_options += [ft.dropdown.Option(key=str(t["id"]), text=t["name"]) for t in teams]

        current_team_value = "none"
        if is_edit and pseudo.get("team_id"):
            current_team_value = str(pseudo["team_id"])

        dd_team = ft.Dropdown(
            label="Equipo asignado",
            options=team_options,
            value=current_team_value,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        dd_status = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("En Proceso"),
                ft.dropdown.Option("Completada"),
            ],
            value=pseudo.get("status", "Pendiente") if is_edit else "Pendiente",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            bgcolor=theme.BG_INPUT,
            border_radius=8,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
        )

        general_error = ft.Text("", size=12, color=theme.ERROR_COLOR, visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_pseudo(evt):
            if not txt_name.value:
                general_error.value = "El nombre del meta es obligatorio."
                general_error.visible = True
                general_error.update()
                return

            team_id = None if dd_team.value == "none" else int(dd_team.value)

            if is_edit:
                update_pseudo_project(
                    pseudo["id"], project["id"], team_id,
                    txt_name.value, txt_description.value, dd_status.value,
                )
            else:
                insert_pseudo_project(
                    project["id"], team_id,
                    txt_name.value, txt_description.value, dd_status.value,
                )

            close_dialog(evt)
            if on_saved:
                on_saved()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Editar Meta" if is_edit else "Nuevo Meta",
                            color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=17),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [txt_name, txt_description, dd_team, dd_status, general_error],
                    tight=True,
                    spacing=14,
                ),
            ),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.OutlinedButton(content=ft.Text("Cancelar", color=theme.TEXT_PRIMARY), on_click=close_dialog),
                        ft.ElevatedButton(
                            content=ft.Text("Guardar", color="#FFFFFF"),
                            bgcolor=theme.ACCENT_COLOR,
                            on_click=save_pseudo,
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

    # ---------- Build principal ----------

    def build(self) -> ft.Container:
        header = ft.Row([
            ft.Column([
                ft.Text("Proyectos", size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ft.Text("Administra los proyectos de desarrollo en curso", size=13, color=theme.TEXT_SECONDARY),
            ], spacing=2),
            ft.Container(expand=True),
            ft.ElevatedButton(
                content=ft.Text("Nuevo Proyecto", size=13, color="#FFFFFF"),
                bgcolor=theme.ACCENT_COLOR,
                on_click=lambda e: self.open_create_modal(),
            )
        ])

        self.projects_container.content = self._build_projects_grid()

        return ft.Container(
            content=ft.Column([
                header,
                ft.Container(height=20),
                self.projects_container
            ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO),
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )