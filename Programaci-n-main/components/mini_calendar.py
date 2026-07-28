import calendar
import datetime
import flet as ft
import theme

MESES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
DIAS_ES = ["L", "M", "M", "J", "V", "S", "D"]


def _day_cell(day_number, is_today, is_current_month):
    if day_number == 0:
        return ft.Container(width=30, height=30)

    text_color = theme.TEXT_MUTED if not is_current_month else theme.TEXT_PRIMARY
    return ft.Container(
        content=ft.Text(str(day_number), size=12, color="#FFFFFF" if is_today else text_color),
        width=30,
        height=30,
        border_radius=15,
        bgcolor=theme.INDIGO if is_today else "transparent",
        alignment=ft.Alignment.CENTER,
    )


def build_mini_calendar(year: int = None, month: int = None) -> ft.Container:
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month

    calendar.setfirstweekday(calendar.MONDAY)
    weeks = calendar.monthcalendar(year, month)

    header = ft.Row(
        [
            ft.Text("Vista rápida", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
        ]
    )

    month_nav = ft.Row(
        [
            ft.Icon(ft.Icons.CHEVRON_LEFT_ROUNDED, size=18, color=theme.TEXT_SECONDARY),
            ft.Text(f"{MESES_ES[month]} {year}", size=13, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
            ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=18, color=theme.TEXT_SECONDARY),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    weekday_row = ft.Row(
        [
            ft.Container(
                content=ft.Text(d, size=11, color=theme.TEXT_MUTED),
                width=30,
                height=22,
                alignment=ft.Alignment.CENTER,
            )
            for d in DIAS_ES
        ],
        spacing=2,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    week_rows = []
    for week in weeks:
        cells = []
        for d in week:
            is_today = d == today.day and month == today.month and year == today.year
            cells.append(_day_cell(d, is_today, is_current_month=True))
        week_rows.append(ft.Row(cells, spacing=2, alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(height=10),
                month_nav,
                ft.Container(height=8),
                weekday_row,
                ft.Column(week_rows, spacing=2),
            ]
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=theme.PADDING_CARD,
        expand=True,
    )
