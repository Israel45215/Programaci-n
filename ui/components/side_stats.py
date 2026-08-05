import flet as ft
import theme

def build_side_stats() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Estadísticas", size=14.5, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                ft.Container(height=10),
                ft.Text("Resumen general del equipo y rendimiento activo de la semana.", size=12, color=theme.TEXT_SECONDARY),
            ],
            spacing=4,
        ),
        bgcolor=theme.BG_CARD,
        border_radius=theme.RADIUS_CARD,
        padding=20,
        expand=True,
    )