import flet as ft
import theme
from dao.team_dao import get_all_teams
from dao.team_rating_dao import insert_team_rating, get_latest_ratings_all_teams, get_latest_rating_by_team

METRICS = [
    ("quality", "Calidad"),
    ("deadlines", "Cumplimiento de plazos"),
    ("communication", "Comunicacion"),
    ("collaboration", "Colaboracion"),
]


class TeamRatingCard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.teams = get_all_teams()

        self.metric_values = {key: 5 for key, _ in METRICS}
        self.metric_value_texts = {}

        self.team_dropdown = ft.Dropdown(
            label="Equipo",
            options=[ft.dropdown.Option(str(t["id"]), t["name"]) for t in self.teams],
            border_color=theme.BORDER_SOFT,
            expand=True,
        )

        self.comment_field = ft.TextField(
            label="Comentario (opcional)",
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=theme.BORDER_SOFT,
        )

        self.ratings_list = ft.Column(spacing=10)
        self._refresh_ratings_list()

        self.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=theme.GREEN)
        if self.snack_bar not in self.page.overlay:
            self.page.overlay.append(self.snack_bar)

    def _metric_slider_row(self, key: str, label: str) -> ft.Column:
        value_text = ft.Text(str(self.metric_values[key]), size=13, weight=ft.FontWeight.BOLD,
                              color=theme.TEXT_PRIMARY)
        self.metric_value_texts[key] = value_text

        def on_change(e, key=key, value_text=value_text):
            value = round(e.control.value)
            self.metric_values[key] = value
            value_text.value = str(value)
            value_text.update()

        slider = ft.Slider(
            min=1, max=10, divisions=9,
            value=self.metric_values[key],
            active_color=theme.ACCENT_COLOR,
            on_change=on_change,
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(label, size=12.5, color=theme.TEXT_SECONDARY),
                        ft.Container(expand=True),
                        value_text,
                    ],
                ),
                slider,
            ],
            spacing=0,
        )

    def _team_name(self, team_id) -> str:
        for t in self.teams:
            if t["id"] == team_id:
                return t["name"]
        return "Equipo eliminado"

    def _rating_row(self, rating: dict) -> ft.Container:
        avg = (rating["quality"] + rating["deadlines"] + rating["communication"] + rating["collaboration"]) / 4
        breakdown = (
            f'Calidad {rating["quality"]:.0f} - Plazos {rating["deadlines"]:.0f} - '
            f'Comunicacion {rating["communication"]:.0f} - Colaboracion {rating["collaboration"]:.0f}'
        )

        info_lines = [
            ft.Text(self._team_name(rating["team_id"]), size=13.5,
                     weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
            ft.Text(breakdown, size=11, color=theme.TEXT_MUTED),
        ]
        if rating.get("comment"):
            info_lines.append(
                ft.Text(f'"{rating["comment"]}"', size=11.5, italic=True, color=theme.TEXT_SECONDARY)
            )
        info_lines.append(ft.Text(rating["created_at"], size=10.5, color=theme.TEXT_MUTED))

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(info_lines, spacing=2, expand=True),
                    ft.Container(
                        content=ft.Text(f"{avg:.1f}", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        bgcolor=theme.GREEN if avg >= 7 else (theme.ACCENT_COLOR if avg >= 4 else theme.ERROR_COLOR),
                        width=40, height=40, border_radius=20,
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=theme.BG_CARD_ALT,
            padding=12,
            border_radius=8,
        )

    def _refresh_ratings_list(self):
        latest = get_latest_ratings_all_teams()
        if not latest:
            self.ratings_list.controls = [
                ft.Text("Aun no se ha calificado a ningun equipo.", size=12.5, color=theme.TEXT_MUTED)
            ]
            return
        rows = [self._rating_row(r) for r in latest.values()]
        self.ratings_list.controls = rows

    def _open_dialog(self, dialog: ft.AlertDialog):
        if hasattr(self.page, "open"):
            self.page.open(dialog)
        else:
            self.page.dialog = dialog
            dialog.open = True
            if dialog not in self.page.overlay:
                self.page.overlay.append(dialog)
            self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog):
        dialog.open = False
        if hasattr(self.page, "close"):
            self.page.close(dialog)
        self.page.update()

    def _show_snack(self, message: str, color: str):
        self.snack_bar.content = ft.Text(message, color="#FFFFFF")
        self.snack_bar.bgcolor = color
        if hasattr(self.page, "open"):
            self.page.open(self.snack_bar)
        else:
            self.snack_bar.open = True
            self.page.update()

    def _save_rating(self, e):
        if not self.team_dropdown.value:
            self._show_snack("Selecciona un equipo antes de guardar.", theme.ERROR_COLOR)
            return

        team_id = int(self.team_dropdown.value)
        existing = get_latest_rating_by_team(team_id)

        if existing:
            self._confirm_overwrite(team_id)
        else:
            self._perform_save(team_id)

    def _confirm_overwrite(self, team_id: int):
        team_name = self._team_name(team_id)

        def on_confirm(e):
            self._close_dialog(dialog)
            self._perform_save(team_id)

        def on_cancel(e):
            self._close_dialog(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sobrescribir calificacion"),
            content=ft.Text(
                f'"{team_name}" ya tiene una calificacion registrada. '
                f"Quieres reemplazarla por la nueva?"
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.ElevatedButton(
                    "Si, sobrescribir",
                    bgcolor=theme.ERROR_COLOR,
                    color="#FFFFFF",
                    on_click=on_confirm,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._open_dialog(dialog)

    def _perform_save(self, team_id: int):
        insert_team_rating(
            team_id=team_id,
            quality=self.metric_values["quality"],
            deadlines=self.metric_values["deadlines"],
            communication=self.metric_values["communication"],
            collaboration=self.metric_values["collaboration"],
            comment=self.comment_field.value or "",
        )

        self.comment_field.value = ""
        self._refresh_ratings_list()
        self.page.update()
        self._show_snack("Calificacion guardada correctamente.", theme.GREEN)

    def build(self) -> ft.Container:
        sliders = ft.Column(
            [self._metric_slider_row(key, label) for key, label in METRICS],
            spacing=14,
        )

        form = ft.Column(
            [
                ft.Text("Calificar equipo", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Evalua el desempeno del equipo en base a estas metricas.",
                        size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=12),
                self.team_dropdown,
                ft.Container(height=8),
                sliders,
                ft.Container(height=8),
                self.comment_field,
                ft.Container(height=8),
                ft.ElevatedButton(
                    "Guardar calificacion",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    bgcolor=theme.ACCENT_COLOR,
                    color="#FFFFFF",
                    on_click=self._save_rating,
                ),
            ],
            spacing=4, expand=1,
        )

        history = ft.Column(
            [
                ft.Text("Ultimas calificaciones", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Text("Calificacion mas reciente registrada por equipo.",
                        size=12, color=theme.TEXT_SECONDARY),
                ft.Container(height=12),
                self.ratings_list,
            ],
            spacing=4, expand=1,
        )

        return ft.Container(
            content=ft.Row([form, history], spacing=24,
                            vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor=theme.BG_CARD,
            border_radius=theme.RADIUS_CARD,
            padding=20,
        )
