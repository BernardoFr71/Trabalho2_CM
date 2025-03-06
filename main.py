import logging
import flet as ft
from layout import create_appbar
from settings import Settings
from solitaire import Solitaire

# logging.basicConfig(level=logging.DEBUG)

def main(page: ft.Page):
    page.title = "Flet Solitaire"  # Título da janela
    page.window_width = 1000  # Largura da janela
    page.window_height = 700  # Altura da janela
    page.window_resizable = False  # Impede que o usuário redimensione a janela

    def on_new_game(settings):
        if hasattr(page, 'solitaire'):
            page.controls.pop()  # Remove o jogo atual
        new_solitaire = Solitaire(settings, on_win)
        page.solitaire = new_solitaire  # Armazena o objeto solitaire na página
        page.add(new_solitaire)
        
        # Referência ao texto do temporizador na barra de aplicativos
        page.solitaire.timer_text = page.appbar.actions[4]  # Ajuste o índice conforme necessário
        
        # Inicia o temporizador
        page.solitaire.start_timer()
        
        page.update()

    def on_win():
        page.add(ft.AlertDialog(title=ft.Text("YOU WIN!"), open=True, on_dismiss=lambda e: page.controls.pop()))
        page.update()

    settings = Settings()
    create_appbar(page, settings, on_new_game)

    solitaire = Solitaire(settings, on_win)
    page.solitaire = solitaire  # Armazena o objeto solitaire na página
    page.add(solitaire)

ft.app(target=main, assets_dir="assets")
