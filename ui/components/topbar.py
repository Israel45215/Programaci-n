import flet as ft
import theme

class Topbar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page_ref = page
        self.bgcolor = theme.BG_SIDEBAR
        self.padding = 12
        
        self.content = ft.Row(
            [
                # Barra de búsqueda
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SEARCH, color=theme.TEXT_SECONDARY, size=18),
                            ft.TextField(
                                hint_text="Buscar en DevTrack...",
                                hint_style=ft.TextStyle(color=theme.TEXT_SECONDARY, size=14),
                                text_style=ft.TextStyle(color=theme.TEXT_PRIMARY, size=14),
                                border=ft.InputBorder.NONE,
                                filled=False,
                                dense=True,
                                content_padding=0,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor=theme.BG_MAIN,
                    border_radius=8,
                    padding=10,
                    width=280,
                ),
                
                ft.Row(
                    [
                        ft.Container(
                            content=ft.CircleAvatar(
                                radius=16,
                                background_image_src="https://picsum.photos/100",
                            ),
                            padding=5,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )