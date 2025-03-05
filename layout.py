import flet as ft
from settings import SettingsDialog

def create_appbar(page, settings, on_new_game):
    def new_game_clicked(e):
        on_new_game(settings)

    def show_rules(e):
        page.dialog = rules_dialog
        rules_dialog.open = True
        page.update()

    def show_settings(e):
        page.dialog = SettingsDialog(settings, on_new_game)
        page.dialog.open = True
        page.update()

    def undo_move(e):
        if hasattr(page, 'solitaire'):
            page.solitaire.undo()
            page.update()

    def save_game(e):
        if hasattr(page, 'solitaire'):
            page.solitaire.save_game()
            print("Jogo salvo com sucesso!")

    def load_game(e):
        if hasattr(page, 'solitaire'):
            page.solitaire.load_game()
            page.update()
            print("Jogo carregado com sucesso!")

    page.appbar = ft.AppBar(
        leading=ft.Image(src=f"/images/card.png"),  # Ícone do jogo
        leading_width=40,  # Largura do ícone
        title=ft.Text("Flet Solitaire"),  # Título do jogo
        bgcolor=ft.colors.SURFACE_VARIANT,  # Cor de fundo
        actions=[
            ft.TextButton("New game", on_click=new_game_clicked),
            ft.TextButton("Undo", on_click=undo_move),
            ft.TextButton("Save", on_click=save_game),
            ft.TextButton("Load", on_click=load_game),
            ft.TextButton("Rules", on_click=show_rules),
            ft.IconButton(ft.icons.SETTINGS, on_click=show_settings),
        ],
    )

    rules_md = ft.Markdown(
        """
        Klondike is played with a standard 52-card deck, without Jokers.
        ... (resto das regras)
        """
    )

    rules_dialog = ft.AlertDialog(
        title=ft.Text("Solitaire rules"),
        content=rules_md,
        on_dismiss=lambda e: print("Dialog dismissed!")
    )