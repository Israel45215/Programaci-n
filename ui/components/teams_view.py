import flet as ft
import theme
from dao.team_dao import get_all_teams, insert_team, update_team, delete_team, init_teams_db
from dao.pseudo_project_dao import get_pseudo_projects_by_team, init_pseudo_projects_db
from dao.employee_dao import get_all_employees, get_employees_by_team, set_team_employees, init_employee_team_db


class TeamsView:
    def __init__(self, page: ft.Page):
        self.page = page
        init_teams_db()
        init_pseudo_projects_db()
        init_employee_team_db()
        self.teams = get_all_teams()
        self.teams_list_container = ft.Container()

    def refresh_ui(self):
        self.teams = get_all_teams()
        self.teams_list_container.content = self._build_teams_list()
        self.page.update()

    def _team_pseudo_count(self, team_id) -> int:
        return len(get_pseudo_projects_by_team(team_id))

    def _team_card(self, team: dict) -> ft.Container:
        assigned_employees = get_employees_by_team(team["id"])
        members = ", ".join(e["name"] for e in assigned_employees) if assigned_employees else "Sin integrantes asignados"
        pseudo_count = self._team_pseudo_count(team["id"])

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.GROUPS_ROUNDED, color=theme.ACCENT_COLOR, size=20),
                                width=40,
                                height=40,
                                border_radius=10,
                                bgcolor=theme.BG_INPUT,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Text(team["name"], size=15, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                    ft.Text(f"{pseudo_count} meta(s) asignado(s)", size=11.5, color=theme.TEXT_SECONDARY),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=theme.TEXT_SECONDARY,
                                icon_size=18,
                                on_click=lambda e, t=team: self.open_edit_modal(t),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=theme.ERROR_COLOR,
                                icon_size=18,
                                on_click=lambda e, t=team: self.confirm_delete_team(t),
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(team.get("description") or "Sin descripción.", size=12.5, color=theme.TEXT_SECONDARY),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_OUTLINE_ROUNDED, size=14, color=theme.TEXT_MUTED),
                            ft.Text(members, size=12, color=theme.TEXT_MUTED),
                        ],
                        spacing=6,
                    ),
                ],
            ),
            bgcolor=theme.BG_CARD,
            border_radius=theme.RADIUS_CARD,
            padding=18,
            expand=True,
        )

    def _build_teams_list(self):
        if not self.teams:
            return ft.Container(
                content=ft.Text("Aún no hay equipos creados. Usa 'Nuevo Equipo' para empezar.",
                                 color=theme.TEXT_SECONDARY, size=13),
                alignment=ft.Alignment.CENTER,
                padding=30,
            )

        rows = []
        for i in range(0, len(self.teams), 2):
            row_teams = self.teams[i:i + 2]
            row_cards = [self._team_card(t) for t in row_teams]
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True))
            rows.append(ft.Row(row_cards, spacing=16))

        return ft.Column(rows, spacing=16)

    def open_create_modal(self):
        self._open_form_modal(team=None)

    def open_edit_modal(self, team: dict):
        self._open_form_modal(team=team)

    def _open_form_modal(self, team):
        is_edit = team is not None

        txt_name = ft.TextField(
            label="Nombre del equipo",
            value=team["name"] if is_edit else "",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        txt_description = ft.TextField(
            label="Descripción del equipo",
            value=team.get("description") if is_edit else "",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        all_employees = get_all_employees()
        assigned_ids = {e["id"] for e in get_employees_by_team(team["id"])} if is_edit else set()

        employee_checkboxes = [
            ft.Checkbox(
                label=emp["name"],
                value=(emp["id"] in assigned_ids),
                data=emp["id"],
                active_color=theme.ACCENT_COLOR,
                label_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
            )
            for emp in all_employees
        ]

        if all_employees:
            members_section = ft.Column(
                [
                    ft.Text("Integrantes", size=12.5, color=theme.TEXT_SECONDARY),
                    ft.Container(
                        content=ft.Column(employee_checkboxes, spacing=2, scroll=ft.ScrollMode.AUTO),
                        height=140,
                        bgcolor=theme.BG_INPUT,
                        border_radius=8,
                        padding=8,
                    ),
                ],
                spacing=6,
            )
        else:
            members_section = ft.Text(
                "Aún no hay empleados registrados. Créalos primero en 'Empleados'.",
                size=12, color=theme.TEXT_MUTED,
            )

        general_error = ft.Text("", size=12, color=theme.ERROR_COLOR, visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_team(evt):
            if not txt_name.value:
                general_error.value = "El nombre del equipo es obligatorio."
                general_error.visible = True
                general_error.update()
                return

            selected_employee_ids = [cb.data for cb in employee_checkboxes if cb.value]

            if is_edit:
                update_team(team["id"], txt_name.value, txt_description.value, "")
                set_team_employees(team["id"], selected_employee_ids)
            else:
                nuevo_id = insert_team(txt_name.value, txt_description.value, "")
                set_team_employees(nuevo_id, selected_employee_ids)

            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Editar Equipo" if is_edit else "Nuevo Equipo",
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
                    [txt_name, txt_description, members_section, general_error],
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
                            on_click=save_team,
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

    def confirm_delete_team(self, team: dict):
        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def execute_delete(evt):
            delete_team(team["id"])
            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Eliminar Equipo", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=400,
                content=ft.Text(
                    f'¿Eliminar el equipo "{team["name"]}"? Esta acción no se puede deshacer.',
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

    def _build_header(self) -> ft.Row:
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Gestión de Equipos", size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text(
                            "Crea y administra los equipos encargados de cada meta.",
                            size=13, color=theme.TEXT_SECONDARY,
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.ADD, size=16, color="#FFFFFF"), ft.Text("Nuevo Equipo", color="#FFFFFF")],
                        spacing=6,
                    ),
                    bgcolor=theme.ACCENT_COLOR,
                    on_click=lambda e: self.open_create_modal(),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def build(self) -> ft.Container:
        header = self._build_header()
        self.teams_list_container.content = self._build_teams_list()

        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20),
                    self.teams_list_container,
                ],
                spacing=0,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )