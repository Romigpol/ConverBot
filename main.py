import threading
import flet as ft
from bot_d import run_bot

def main(page: ft.Page):
    page.title = "Panel de Control - ConverBot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.window.width = 500
    page.window.height = 400

    description_text = (
        "Sistema automatizado de conversión local de documentación de documentos y archivos  multimedia para tu servidor de discord."
    )

    title = ft.Text("ConverBot", size=22, weight=ft.FontWeight.BOLD)
    description = ft.Text(description_text, size=14, text_align=ft.TextAlign.CENTER)

    invite_button = ft.Button(
        content="Invita a ConverBot a tu servidor",
        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
        url="https://discord.com/oauth2/authorize?client_id=1561402510873329714",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
    )

    page.add(
        ft.Column(
            [title, description, invite_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        )
    )


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    ft.run(main)