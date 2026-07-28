import flet as ft
import theme
from components import projects_repository as repo


def _field_label(text_value: str) -> ft.Text:
    return ft.Text(text_value, size=12.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY)


def _date_field(hint="día/mes/año") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=theme.TEXT_MUTED, size=13),
        text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
        bgcolor=theme.BG_INPUT,
        border_color=theme.BORDER_SOFT,
        focused_border_color=theme.INDIGO,
        border_radius=10,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        suffix_icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
    )


def _name_field(hint="Ej. Rediseño de Plataforma Web") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=theme.TEXT_MUTED, size=13),
        text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=13),
        bgcolor=theme.BG_INPUT,
        border_color=theme.BORDER_SOFT,
        focused_border_color=theme.INDIGO,
        border_radius=10,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )


def _pill_button(label, bgcolor, text_color, on_click, icon=None):
    row_items = []
    if icon:
        row_items.append(ft.Icon(icon, size=16, color=text_color))
    row_items.append(ft.Text(label, size=13, weight=ft.FontWeight.W_600, color=text_color))
    return ft.Container(
        content=ft.Row(row_items, spacing=6, tight=True, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=bgcolor,
        padding=ft.Padding.symmetric(horizontal=18, vertical=11),
        border_radius=theme.RADIUS_PILL,
        on_click=on_click,
        ink=True,
    )


def _dialog_title(title_text, on_close) -> ft.Row:
    return ft.Row(
        [
            ft.Text(title_text, size=16, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=18, color=theme.TEXT_SECONDARY),
                on_click=on_close,
                ink=True,
                border_radius=16,
                padding=6,
            ),
        ]
    )


def _icon_action_button(icon, bg, color, on_click):
    return ft.Container(
        content=ft.Icon(icon, size=16, color=color),
        width=32,
        height=32,
        bgcolor=bg,
        border_radius=8,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        ink=True,
    )


class ProjectsView:
    """Vista de Proyectos: tabla + modales de crear/editar/borrar."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.projects = []
        self.load_error = None
        self._load_projects()

        self.table_rows = ft.Column(spacing=0)
        self.error_banner = ft.Container(visible=False)
        self.root = self._build_root()
        self._build_rows()
        self._update_error_banner()

    def _load_projects(self):
        """Trae los proyectos desde PostgreSQL. Si falla, guarda el error para mostrarlo."""
        try:
            self.projects = repo.fetch_all()
            self.load_error = None
        except Exception as db_err:
            self.projects = []
            self.load_error = (
                "No se pudo conectar con la base de datos. Revisa db_config.py "
                f"(host, usuario, password). Detalle: {db_err}"
            )

    def _update_error_banner(self):
        if self.load_error:
            self.error_banner.visible = True
            self.error_banner.content = ft.Row(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, size=18, color="#FCA5A5"),
                    ft.Text(self.load_error, size=12, color="#FCA5A5", expand=True),
                ],
                spacing=8,
            )
            self.error_banner.bgcolor = ft.Colors.with_opacity(0.12, "#EF4444")
            self.error_banner.border_radius = 10
            self.error_banner.padding = 12
            self.error_banner.margin = ft.Margin.only(bottom=14)
        else:
            self.error_banner.visible = False

    # ---------- construcción de la vista principal ----------

    def _build_root(self) -> ft.Container:
        header = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Proyectos", size=24, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text(
                            "Gestiona los proyectos de la empresa y su estado",
                            size=12.5,
                            color=theme.TEXT_SECONDARY,
                        ),
                    ],
                    spacing=4,
                ),
                ft.Container(expand=True),
                _pill_button(
                    "Crear proyecto",
                    theme.INDIGO,
                    "#FFFFFF",
                    self._open_create_dialog,
                    icon=ft.Icons.ADD_ROUNDED,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        column_header = ft.Container(
            content=ft.Row(
                [
                    ft.Container(ft.Text("ID", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED), width=90),
                    ft.Container(
                        ft.Text("NOMBRE", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED), expand=3
                    ),
                    ft.Container(
                        ft.Text("FECHA INICIO", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED),
                        expand=2,
                    ),
                    ft.Container(
                        ft.Text("FECHA ENTREGA", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED),
                        expand=2,
                    ),
                    ft.Container(
                        ft.Text("EDITAR", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED), width=90
                    ),
                ]
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            border=ft.Border.only(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
        )

        table_card = ft.Container(
            content=ft.Column([column_header, self.table_rows], spacing=0),
            bgcolor=theme.BG_CARD,
            border_radius=theme.RADIUS_CARD,
        )

        return ft.Container(
            content=ft.Column(
                [header, ft.Container(height=18), self.error_banner, table_card],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.only(left=28, right=28, bottom=24),
            expand=True,
        )

    def build(self) -> ft.Container:
        return self.root

    # ---------- filas de la tabla ----------

    def _refresh_table(self):
        self._load_projects()
        self._build_rows()
        self._update_error_banner()
        self.page.update()

    def _build_rows(self):
        rows = []
        for project in self.projects:
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                ft.Text(project["display_id"], size=12.5, color=theme.TEXT_SECONDARY), width=90
                            ),
                            ft.Container(
                                ft.Text(project["name"], size=13, color=theme.TEXT_PRIMARY), expand=3
                            ),
                            ft.Container(
                                ft.Text(project["start"], size=12.5, color=theme.TEXT_SECONDARY), expand=2
                            ),
                            ft.Container(
                                ft.Text(project["end"], size=12.5, color=theme.TEXT_SECONDARY), expand=2
                            ),
                            ft.Container(
                                ft.Row(
                                    [
                                        _icon_action_button(
                                            ft.Icons.EDIT_ROUNDED,
                                            ft.Colors.with_opacity(0.15, theme.BLUE),
                                            theme.BLUE,
                                            lambda e, p=project: self._open_edit_dialog(p),
                                        ),
                                        _icon_action_button(
                                            ft.Icons.DELETE_ROUNDED,
                                            "#EF4444",
                                            "#FFFFFF",
                                            lambda e, p=project: self._open_delete_dialog(p),
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                width=90,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                    border=ft.Border.only(bottom=ft.BorderSide(1, theme.BORDER_SOFT)),
                )
            )
        self.table_rows.controls = rows

    # ---------- diálogo: crear proyecto ----------

    def _open_create_dialog(self, e):
        name_field = _name_field()
        start_field = _date_field()
        end_field = _date_field()
        general_error = ft.Text("", size=12, color="#F87171", visible=False)

        def close_dialog(e=None):
            self.page.pop_dialog()

        def save(e=None):
            valid = True
            if not name_field.value:
                name_field.error_text = "Este campo es requerido"
                valid = False
            else:
                name_field.error_text = None

            if not start_field.value:
                start_field.error_text = "Requerido"
                valid = False
            else:
                start_field.error_text = None

            if not end_field.value:
                end_field.error_text = "Requerido"
                valid = False
            else:
                end_field.error_text = None

            if not valid:
                self.page.update()
                return

            try:
                repo.create(name_field.value, start_field.value, end_field.value)
            except ValueError as ve:
                general_error.value = str(ve)
                general_error.visible = True
                self.page.update()
                return
            except Exception as db_err:
                general_error.value = f"Error al guardar en la base de datos: {db_err}"
                general_error.visible = True
                self.page.update()
                return

            close_dialog()
            self._refresh_table()

        dialog = ft.AlertDialog(
            modal=True,
            title=_dialog_title("Crear proyecto", close_dialog),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [
                        _field_label("Nombre del proyecto *"),
                        name_field,
                        ft.Container(height=6),
                        ft.Row(
                            [
                                ft.Column(
                                    [_field_label("Fecha inicio *"), start_field], spacing=6, expand=True
                                ),
                                ft.Column(
                                    [_field_label("Fecha entrega *"), end_field], spacing=6, expand=True
                                ),
                            ],
                            spacing=14,
                        ),
                        ft.Container(height=6),
                        general_error,
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=theme.TEXT_MUTED),
                                    ft.Text(
                                        "El identificador (ID) del proyecto se generará de forma "
                                        "automática al guardar los datos.",
                                        size=11.5,
                                        color=theme.TEXT_MUTED,
                                        expand=True,
                                    ),
                                ],
                                spacing=8,
                            ),
                            bgcolor=theme.BG_INPUT,
                            border_radius=10,
                            padding=12,
                        ),
                    ],
                    spacing=8,
                    tight=True,
                ),
            ),
            actions=[
                _pill_button("Cancelar", "transparent", theme.TEXT_SECONDARY, close_dialog),
                _pill_button("Guardar proyecto", theme.INDIGO, "#FFFFFF", save),
            ],
            bgcolor=theme.BG_CARD,
        )
        self.page.show_dialog(dialog)

    # ---------- diálogo: editar proyecto ----------

    def _open_edit_dialog(self, project):
        name_field = _name_field()
        name_field.value = project["name"]
        start_field = _date_field()
        start_field.value = project["start"]
        end_field = _date_field()
        end_field.value = project["end"]
        general_error = ft.Text("", size=12, color="#F87171", visible=False)

        def close_dialog(e=None):
            self.page.pop_dialog()

        def save(e=None):
            valid = True
            if not name_field.value:
                name_field.error_text = "Este campo es requerido"
                valid = False
            else:
                name_field.error_text = None

            if not start_field.value:
                start_field.error_text = "Requerido"
                valid = False
            else:
                start_field.error_text = None

            if not end_field.value:
                end_field.error_text = "Requerido"
                valid = False
            else:
                end_field.error_text = None

            if not valid:
                self.page.update()
                return

            try:
                repo.update(project["id"], name_field.value, start_field.value, end_field.value)
            except ValueError as ve:
                general_error.value = str(ve)
                general_error.visible = True
                self.page.update()
                return
            except Exception as db_err:
                general_error.value = f"Error al guardar en la base de datos: {db_err}"
                general_error.visible = True
                self.page.update()
                return

            close_dialog()
            self._refresh_table()

        dialog = ft.AlertDialog(
            modal=True,
            title=_dialog_title("Editar proyecto", close_dialog),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    [
                        _field_label("Nombre del proyecto *"),
                        name_field,
                        ft.Container(height=6),
                        ft.Row(
                            [
                                ft.Column(
                                    [_field_label("Fecha inicio *"), start_field], spacing=6, expand=True
                                ),
                                ft.Column(
                                    [_field_label("Fecha entrega *"), end_field], spacing=6, expand=True
                                ),
                            ],
                            spacing=14,
                        ),
                        ft.Container(height=6),
                        general_error,
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=theme.TEXT_MUTED),
                                    ft.Text(
                                        "El identificador (ID) del proyecto se generará de forma "
                                        "automática al guardar los datos.",
                                        size=11.5,
                                        color=theme.TEXT_MUTED,
                                        expand=True,
                                    ),
                                ],
                                spacing=8,
                            ),
                            bgcolor=theme.BG_INPUT,
                            border_radius=10,
                            padding=12,
                        ),
                    ],
                    spacing=8,
                    tight=True,
                ),
            ),
            actions=[
                _pill_button("Cancelar", "transparent", theme.TEXT_SECONDARY, close_dialog),
                _pill_button("Guardar proyecto", theme.INDIGO, "#FFFFFF", save),
            ],
            bgcolor=theme.BG_CARD,
        )
        self.page.show_dialog(dialog)

    # ---------- diálogo: borrar proyecto ----------

    def _open_delete_dialog(self, project):
        general_error = ft.Text("", size=12, color="#F87171", visible=False)

        def close_dialog(e=None):
            self.page.pop_dialog()

        def confirm_delete(e=None):
            try:
                repo.delete(project["id"])
            except Exception as db_err:
                general_error.value = f"Error al borrar en la base de datos: {db_err}"
                general_error.visible = True
                self.page.update()
                return
            close_dialog()
            self._refresh_table()

        dialog = ft.AlertDialog(
            modal=True,
            title=_dialog_title("Borrar proyecto", close_dialog),
            content=ft.Container(
                width=380,
                content=ft.Column(
                    [
                        ft.Text(
                            "Se borrará este proyecto definitivamente de la base de datos.\n"
                            "¿Estás seguro de esta decisión?",
                            size=13,
                            color=theme.TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        general_error,
                    ],
                    spacing=10,
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(vertical=10),
            ),
            actions=[
                _pill_button("Borrar proyecto", "#EF4444", "#FFFFFF", confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=theme.BG_CARD,
        )
        self.page.show_dialog(dialog)
