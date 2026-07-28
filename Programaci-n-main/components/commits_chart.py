import flet as ft
import theme

WEEKS = ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5", "Semana 6"]

# Valores de ejemplo (%) -- reemplazar con datos reales de la BD.
COMMITS_DATA = [55, 78, 82, 40, 90, 60]
PULL_REQUESTS_DATA = [35, 45, 60, 30, 55, 38]

CHART_HEIGHT = 170


def _legend_dot(color, label):
    return ft.Row(
        [
            ft.Container(width=10, height=10, border_radius=5, bgcolor=color),
            ft.Text(label, size=12, color=theme.TEXT_SECONDARY),
        ],
        spacing=6,
    )


def _bar(value, color):
    """Una barra individual, con altura proporcional a value (0-100)."""
    return ft.Container(
        width=12,
        height=max(4, CHART_HEIGHT * (value / 100)),
        bgcolor=color,
        border_radius=ft.BorderRadius.only(top_left=4, top_right=4),
        tooltip=f"{value}%",
    )


def _week_column(week_label, commits_value, pr_value):
    bars = ft.Row(
        [
            _bar(commits_value, theme.INDIGO),
            _bar(pr_value, theme.PURPLE),
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        height=CHART_HEIGHT,
    )
    return ft.Column(
        [bars, ft.Text(week_label, size=10.5, color=theme.TEXT_MUTED)],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )


def _y_axis_labels() -> ft.Column:
    values = [100, 75, 50, 25, 0]
    return ft.Column(
        [ft.Text(f"{v}%", size=10, color=theme.TEXT_MUTED) for v in values],
        spacing=0,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=CHART_HEIGHT,
    )


def build_commits_chart() -> ft.Container:
    week_columns = ft.Row(
        [
            _week_column(week, COMMITS_DATA[i], PULL_REQUESTS_DATA[i])
            for i, week in enumerate(WEEKS)
        ],
        spacing=10,
        expand=True,
    )

    chart_body = ft.Row(
        [
            _y_axis_labels(),
            ft.Container(
                content=week_columns,
                expand=True,
                border=ft.Border.only(left=ft.BorderSide(1, theme.BORDER_SOFT)),
                padding=ft.Padding.only(left=14),
            ),
        ],
        spacing=8,
    )

    header = ft.Row(
        [
            ft.Text("Commits y pull requests", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
            ft.Container(expand=True),
            _legend_dot(theme.INDIGO, "Commits"),
            ft.Container(width=14),
            _legend_dot(theme.PURPLE, "Pull requests"),
        ]
    )

    return ft.Container(
        content=ft.Column([header, ft.Container(height=18), chart_body], expand=True),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=theme.PADDING_CARD,
        expand=True,
    )
