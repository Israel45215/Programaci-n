import calendar
import datetime

import flet as ft
import theme

from dao.task_dao import get_all_tasks_with_details


MESES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

DIAS_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


def build_mini_calendar() -> ft.Container:
    hoy = datetime.date.today()
    tareas = get_all_tasks_with_details()

    fechas_limite = {}

    for tarea in tareas:
        fecha_texto = tarea.get("date")

        if not fecha_texto:
            continue

        try:
            fecha = datetime.datetime.strptime(
                fecha_texto,
                "%Y-%m-%d",
            ).date()
        except (TypeError, ValueError):
            continue

        if (
            fecha.year == hoy.year
            and fecha.month == hoy.month
            and tarea.get("status") != "Completada"
        ):
            fechas_limite.setdefault(fecha.day, []).append(tarea)

    semanas = calendar.Calendar(
        firstweekday=calendar.MONDAY
    ).monthdayscalendar(
        hoy.year,
        hoy.month,
    )

    encabezado_dias = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(
                    dia,
                    size=11,
                    weight=ft.FontWeight.W_600,
                    color=theme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                expand=True,
                alignment=ft.Alignment.CENTER,
            )
            for dia in DIAS_CORTOS
        ],
        spacing=4,
    )

    filas_calendario = []

    for semana in semanas:
        celdas = []

        for dia in semana:
            if dia == 0:
                celdas.append(
                    ft.Container(
                        expand=True,
                        height=42,
                    )
                )
                continue

            es_hoy = dia == hoy.day
            tiene_tareas = dia in fechas_limite

            contenido = ft.Column(
                controls=[
                    ft.Text(
                        str(dia),
                        size=12,
                        weight=(
                            ft.FontWeight.BOLD
                            if es_hoy
                            else ft.FontWeight.W_500
                        ),
                        color=theme.TEXT_PRIMARY,
                    ),
                    ft.Container(
                        width=5,
                        height=5,
                        border_radius=3,
                        bgcolor=(
                            theme.ACCENT_COLOR
                            if tiene_tareas
                            else None
                        ),
                        visible=tiene_tareas,
                    ),
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )

            celdas.append(
                ft.Container(
                    content=contenido,
                    expand=True,
                    height=42,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=(
                        theme.SIDEBAR_ACTIVE_BG
                        if es_hoy
                        else theme.BG_CARD_ALT
                    ),
                    border=ft.Border.all(
                        1,
                        (
                            theme.ACCENT_COLOR
                            if es_hoy
                            else theme.BORDER_SOFT
                        ),
                    ),
                    border_radius=9,
                    tooltip=(
                        f"{len(fechas_limite[dia])} tarea(s) pendiente(s)"
                        if tiene_tareas
                        else None
                    ),
                )
            )

        filas_calendario.append(
            ft.Row(
                controls=celdas,
                spacing=4,
            )
        )

    leyenda = ft.Row(
        controls=[
            ft.Container(
                width=7,
                height=7,
                border_radius=4,
                bgcolor=theme.ACCENT_COLOR,
            ),
            ft.Text(
                "Días con tareas pendientes",
                size=10.5,
                color=theme.TEXT_SECONDARY,
            ),
        ],
        spacing=7,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Calendario",
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    f"{MESES[hoy.month - 1]} {hoy.year}",
                                    size=12,
                                    color=theme.TEXT_SECONDARY,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Icon(
                            ft.Icons.CALENDAR_MONTH_ROUNDED,
                            color=theme.ACCENT_COLOR,
                            size=23,
                        ),
                    ],
                ),
                ft.Container(height=6),
                encabezado_dias,
                ft.Column(
                    controls=filas_calendario,
                    spacing=4,
                ),
                ft.Container(height=4),
                leyenda,
            ],
            spacing=7,
        ),
        bgcolor=theme.BG_CARD,
        border=ft.Border.all(
            1,
            theme.BORDER_SOFT,
        ),
        border_radius=theme.RADIUS_CARD,
        padding=18,
        expand=True,
    )