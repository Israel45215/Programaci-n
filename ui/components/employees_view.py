import flet as ft
import theme
from dao.employee_dao import (
    get_all_employees,
    insert_employee,
    update_employee,
    delete_employee,
    init_employees_db,
    get_teams_by_employee,
    set_employee_teams,
)
from dao.team_dao import get_all_teams, init_teams_db


class EmployeesView:
    def __init__(self, page: ft.Page):
        self.page = page
        init_employees_db()
        init_teams_db()
        self.employees = get_all_employees()
        self.list_container = ft.Container()

    def refresh_ui(self):
        self.employees = get_all_employees()
        self.list_container.content = self._build_list()
        self.page.update()

    def _employee_card(self, employee: dict) -> ft.Container:
        teams = get_teams_by_employee(employee["id"])
        teams_text = ", ".join(t["name"] for t in teams) if teams else "Sin equipos asignados"

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.BADGE_ROUNDED, color=theme.ACCENT_COLOR, size=20),
                                width=40,
                                height=40,
                                border_radius=10,
                                bgcolor=theme.BG_INPUT,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Text(employee["name"], size=15, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=theme.TEXT_SECONDARY,
                                icon_size=18,
                                on_click=lambda e, emp=employee: self.open_edit_modal(emp),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=theme.ERROR_COLOR,
                                icon_size=18,
                                on_click=lambda e, emp=employee: self.confirm_delete(emp),
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.GROUPS_ROUNDED, size=14, color=theme.TEXT_MUTED),
                            ft.Text(teams_text, size=12, color=theme.TEXT_MUTED),
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

    def _build_list(self):
        if not self.employees:
            return ft.Container(
                content=ft.Text(
                    "Aún no hay empleados registrados. Usa 'Nuevo Empleado' para empezar.",
                    color=theme.TEXT_SECONDARY, size=13,
                ),
                alignment=ft.Alignment.CENTER,
                padding=30,
            )

        rows = []
        for i in range(0, len(self.employees), 2):
            row_emp = self.employees[i:i + 2]
            row_cards = [self._employee_card(emp) for emp in row_emp]
            if len(row_cards) == 1:
                row_cards.append(ft.Container(expand=True))
            rows.append(ft.Row(row_cards, spacing=16))

        return ft.Column(rows, spacing=16)

    def open_create_modal(self):
        self._open_form_modal(employee=None)

    def open_edit_modal(self, employee: dict):
        self._open_form_modal(employee=employee)

    def _open_form_modal(self, employee):
        is_edit = employee is not None
        all_teams = get_all_teams()
        assigned_ids = {t["id"] for t in get_teams_by_employee(employee["id"])} if is_edit else set()

        txt_name = ft.TextField(
            label="Nombre del empleado",
            value=employee["name"] if is_edit else "",
            border_color=theme.BORDER_SOFT,
            focused_border_color=theme.ACCENT_COLOR,
            text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13.5),
            bgcolor=theme.BG_INPUT,
            border_radius=8,
        )

        team_checkboxes = [
            ft.Checkbox(
                label=t["name"],
                value=(t["id"] in assigned_ids),
                data=t["id"],
                active_color=theme.ACCENT_COLOR,
                label_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
            )
            for t in all_teams
        ]

        general_error = ft.Text("", size=12, color=theme.ERROR_COLOR, visible=False)

        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def save_employee(evt):
            name_value = (txt_name.value or "").strip()
            if not name_value:
                general_error.value = "El nombre del empleado es obligatorio."
                general_error.visible = True
                general_error.update()
                return

            selected_team_ids = [cb.data for cb in team_checkboxes if cb.value]

            if is_edit:
                update_employee(employee["id"], name_value)
                set_employee_teams(employee["id"], selected_team_ids)
            else:
                nuevo_id = insert_employee(name_value)
                set_employee_teams(nuevo_id, selected_team_ids)

            close_dialog(evt)
            self.refresh_ui()

        if all_teams:
            teams_section = ft.Column(
                [
                    ft.Text("Equipos asignados", size=12.5, color=theme.TEXT_SECONDARY),
                    ft.Container(
                        content=ft.Column(team_checkboxes, spacing=2, scroll=ft.ScrollMode.AUTO),
                        height=140,
                        bgcolor=theme.BG_INPUT,
                        border_radius=8,
                        padding=8,
                    ),
                ],
                spacing=6,
            )
        else:
            teams_section = ft.Text("Aún no hay equipos creados.", size=12, color=theme.TEXT_MUTED)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text(
                        "Editar Empleado" if is_edit else "Nuevo Empleado",
                        color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [txt_name, teams_section, general_error],
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
                            on_click=save_employee,
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

    def confirm_delete(self, employee: dict):
        def close_dialog(evt):
            dialog.open = False
            if hasattr(self.page, "close"):
                self.page.close(dialog)
            self.page.update()

        def execute_delete(evt):
            delete_employee(employee["id"])
            close_dialog(evt)
            self.refresh_ui()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text("Eliminar Empleado", color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=18),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.TEXT_MUTED, icon_size=18, on_click=close_dialog),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD,
            content=ft.Container(
                width=400,
                content=ft.Text(
                    f'¿Eliminar al empleado "{employee["name"]}"? Esta acción no se puede deshacer.',
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
                        ft.Text("Gestión de Empleados", size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text(
                            "Registra empleados y asígnalos a uno o varios equipos.",
                            size=13, color=theme.TEXT_SECONDARY,
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.ADD, size=16, color="#FFFFFF"), ft.Text("Nuevo Empleado", color="#FFFFFF")],
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
        self.list_container.content = self._build_list()

        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20),
                    self.list_container,
                ],
                spacing=0,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )
