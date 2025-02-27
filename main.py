import flet as ft

class Solitario:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Solitário com Flet"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.estado_jogo = None
        self.card_back_image = "default.jpg"
        self.criar_interface()
    
    def criar_interface(self):
        self.page.clean()
        self.titulo = ft.Text("Jogo de Solitário", size=30, weight=ft.FontWeight.BOLD)
        self.iniciar_jogo_btn = ft.ElevatedButton("Iniciar Jogo", on_click=self.iniciar_jogo)
        self.desfazer_btn = ft.ElevatedButton("Desfazer", on_click=self.desfazer, disabled=True)
        self.salvar_btn = ft.ElevatedButton("Salvar Jogo", on_click=self.salvar)
        self.carregar_btn = ft.ElevatedButton("Carregar Jogo", on_click=self.carregar)
        
        self.card_back_options = ["back1.jpg", "back2.jpg", "back3.jpg", "back4.jpg"]
        self.card_back_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(img) for img in self.card_back_options],
            on_change=self.selecionar_imagem_cartas
        )
        
        self.page.add(self.titulo, self.iniciar_jogo_btn, self.desfazer_btn, self.salvar_btn, self.carregar_btn, self.card_back_dropdown)
        self.page.update()
    
    def iniciar_jogo(self, e):
        self.estado_jogo = "Novo jogo iniciado"
        self.desfazer_btn.disabled = False
        self.page.clean()
        self.page.add(ft.Text("Jogo iniciado! Implementação do jogo aqui..."), self.desfazer_btn, self.salvar_btn, self.carregar_btn, self.card_back_dropdown)
        self.page.update()
    
    def desfazer(self, e):
        if self.estado_jogo:
            self.page.clean()
            self.page.add(ft.Text("Última jogada desfeita."), self.iniciar_jogo_btn, self.desfazer_btn, self.salvar_btn, self.carregar_btn, self.card_back_dropdown)
            self.page.update()
    
    def salvar(self, e):
        self.page.clean()
        self.page.add(ft.Text("Jogo salvo com sucesso."), self.iniciar_jogo_btn, self.desfazer_btn, self.salvar_btn, self.carregar_btn, self.card_back_dropdown)
        self.page.update()
    
    def carregar(self, e):
        self.page.clean()
        self.page.add(ft.Text("Jogo carregado."), self.iniciar_jogo_btn, self.desfazer_btn, self.salvar_btn, self.carregar_btn, self.card_back_dropdown)
        self.page.update()
    
    def selecionar_imagem_cartas(self, e):
        self.card_back_image = e.control.value
        self.page.add(ft.Text(f"Imagem traseira das cartas selecionada: {self.card_back_image}"))
        self.page.update()

def main(page: ft.Page):
    Solitario(page)

ft.app(target=main)
