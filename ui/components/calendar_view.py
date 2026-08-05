import calendar as pycalendar
import datetime
import flet as ft
import theme
from dao.task_dao import get_all_tasks_with_details, init_db

MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

WEEKDAY_LABELS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


class CalendarView:
    def __init__(self, page: ft.Page):
        self.page = page
        init_db()
        self.tasks = get_all_tasks_with_details()

        today = datetime.date.today()
        self.today_str = today.strftime("%Y-%m-%d")
        self.current_year = today.year
        self.current_month = today.month
        self.selected_date = self.today_str

        self.calendar_container = ft.Container()

    def refresh_ui(self):
        self.tasks = get_all_tasks_with_details()
        self.calendar_container.content = self._build_calendar_card()
        self.calendar_container.update()

    def _tasks_by_date(self) -> dict:
        grouped = {}
        for t in self.tasks:
            date_str = t.get("date")
            if not date_str:
                continue
            grouped.setdefault(date_str, []).append(t)
        return grouped

    def _status_badge(self, status: str) -> ft.Container:
        color_map = {
            "Completada": (theme.GREEN, "#102A1D"),
            "En Proceso": (theme.BLUE, "#141F48"),
            "Pendiente": ("#F59E0B", "#2D220E"),
        }
        text_color, bg_color = color_map.get(status, (theme.TEXT_SECONDARY, theme.BG_CARD_ALT))
        return ft.Container(
            content=ft.Text(status, size=10.5, weight=ft.FontWeight.W_600, color=text_color),
            bgcolor=bg_color,
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
            border_radius=theme.RADIUS_PILL,
        )

    def _select_date(self, date_str: str):
        self.selected_date = date_str
        self.refresh_ui()

    def _prev_month(self, e):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh_ui()

    def _next_month(self, e):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh_ui()

    def _day_cell(self, day_num, date_str, is_today, is_selected, task_count) -> ft.Container:
        if day_num is None:
            return ft.Container(expand=True, height=64)

        if is_selected:
            bg = theme.SIDEBAR_ACTIVE_BG
        elif is_today:
            bg = theme.HOVER_CARD_BG
        else:
            bg = "transparent"

        border = ft.Border(
            top=ft.BorderSide(1, theme.ACCENT_COLOR), bottom=ft.BorderSide(1, theme.ACCENT_COLOR),
            left=ft.BorderSide(1, theme.ACCENT_COLOR), right=ft.BorderSide(1, theme.ACCENT_COLOR),
        ) if (is_today and not is_selected) else None

        children = [
            ft.Text(
                str(day_num), size=13,
                weight=ft.FontWeight.W_700 if (is_today or is_selected) else ft.FontWeight.NORMAL,
                color=theme.TEXT_PRIMARY if (is_today or is_selected) else theme.TEXT_SECONDARY,
            ),
        ]
        if task_count > 0:
            children.append(
                ft.Container(
                    content=ft.Text(str(task_count), size=9, color="#FFFFFF", weight=ft.FontWeight.BOLD),
                    bgcolor=theme.ACCENT_COLOR,
                    width=16, height=16, border_radius=8,
                    alignment=ft.Alignment.CENTER,
                )
            )

        return ft.Container(
            content=ft.Column(children, spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               alignment=ft.MainAxisAlignment.CENTER),
            expand=True, height=64,
            bgcolor=bg,
            border=border,
            border_radius=8,
            alignment=ft.Alignment.CENTER,
            on_click=lambda e, d=date_str: self._select_date(d),
            ink=True,
        )

    def _build_calendar_grid(self) -> ft.Column:
        tasks_by_date = self._tasks_by_date()
        first_weekday, days_in_month = pycalendar.monthrange(self.current_year, self.current_month)

        cells = [self._day_cell(None, None, False, False, 0) for _ in range(first_weekday)]

        for day in range(1, days_in_month + 1):
            date_str = f"{self.current_year:04d}-{self.current_month:02d}-{day:02d}"
            is_today = date_str == self.today_str
            is_selected = date_str == self.selected_date
            count = len(tasks_by_date.get(date_str, []))
            cells.append(self._day_cell(day, date_str, is_today, is_selected, count))

        while len(cells) % 7 != 0:
            cells.append(self._day_cell(None, None, False, False, 0))

        weeks = [ft.Row(cells[i:i + 7], spacing=6) for i in range(0, len(cells), 7)]
        return ft.Column(weeks, spacing=6)

    def _build_day_tasks_panel(self) -> ft.Column:
        if not self.selected_date:
            return ft.Column(
                [ft.Text("Selecciona un día para ver sus tareas.", size=13, color=theme.TEXT_MUTED)]
            )

        tasks_by_date = self._tasks_by_date()
        day_tasks = tasks_by_date.get(self.selected_date, [])
        date_obj = datetime.date.fromisoformat(self.selected_date)
        header = ft.Text(
            f"Tareas del {date_obj.day} de {MONTH_NAMES[date_obj.month - 1]}",
            size=14, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY,
        )

        if not day_tasks:
            return ft.Column(
                [header, ft.Container(height=10),
                 ft.Text("No hay tareas con fecha límite este día.", size=12.5, color=theme.TEXT_MUTED)],
                spacing=4,
            )

        rows = []
        for t in day_tasks:
            pseudo_label = t.get("pseudo_project_name") or "Sin asignar"
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(t["title"], size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                    ft.Text(f'{t.get("assigned") or "Sin asignar"} · {pseudo_label}',
                                            size=10.5, color=theme.TEXT_MUTED),
                                ],
                                spacing=2, expand=True,
                            ),
                            self._status_badge(t["status"]),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=theme.BG_CARD_ALT,
                    padding=12,
                    border_radius=8,
                )
            )

        return ft.Column(
            [header, ft.Container(height=10), ft.Column(rows, spacing=8)],
            spacing=4,
        )

    def _build_calendar_card(self) -> ft.Row:
        month_label = f"{MONTH_NAMES[self.current_month - 1]} {self.current_year}"

        nav_header = ft.Row(
            [
                ft.Text(month_label, size=16, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, icon_color=theme.TEXT_SECONDARY, on_click=self._prev_month),
                ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, icon_color=theme.TEXT_SECONDARY, on_click=self._next_month),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        weekday_labels = ft.Row(
            [
                ft.Container(
                    content=ft.Text(d, size=11, weight=ft.FontWeight.BOLD, color=theme.TEXT_MUTED),
                    expand=True, alignment=ft.Alignment.CENTER,
                )
                for d in WEEKDAY_LABELS
            ],
            spacing=6,
        )

        grid_card = ft.Container(
            content=ft.Column([nav_header, ft.Container(height=14), weekday_labels,
                                ft.Container(height=6), self._build_calendar_grid()]),
            bgcolor=theme.BG_CARD,
            border_radius=theme.RADIUS_CARD,
            padding=20,
            expand=2,
        )

        day_panel = ft.Container(
            content=self._build_day_tasks_panel(),
            bgcolor=theme.BG_CARD,
            border_radius=theme.RADIUS_CARD,
            padding=20,
            expand=1,
        )

        # vertical_alignment=START: evita que el panel de tareas quede
        # centrado verticalmente respecto a la tarjeta del calendario.
        return ft.Row(
            [grid_card, day_panel],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def build(self) -> ft.Container:
        header = ft.Column(
            [
                ft.Text("Calendario", size=22, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ft.Text("Visualiza las fechas límite de tus tareas", size=13, color=theme.TEXT_SECONDARY),
            ],
            spacing=2,
        )

        self.calendar_container.content = self._build_calendar_card()

        return ft.Container(
            content=ft.Column(
                [header, ft.Container(height=20), self.calendar_container],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            padding=ft.Padding.only(left=28, right=28, top=10, bottom=24),
            expand=True,
        )