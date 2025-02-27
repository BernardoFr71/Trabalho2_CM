import flet as ft
import random

# Constantes
CARD_WIDTH = 70
CARD_HEIGHT = 100
DROP_PROXIMITY = 20
CARD_OFFSET = 20
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

# Classes
class Suite:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Rank:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Slot(ft.Container):
    def __init__(self, solitaire, top=0, left=0, border=None):
        super().__init__()
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.top = top
        self.left = left
        self.border = border
        self.pile = []  # Lista de cartas no slot
        self.solitaire = solitaire

    def get_top_card(self):
        """Retorna a carta no topo da pilha, se houver."""
        if self.pile:
            return self.pile[-1]
        return None

class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.solitaire = solitaire
        self.slot = None
        self.left = 0
        self.top = 0
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.double_click

        self.content = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=ft.border_radius.all(6),
            content=ft.Image(src="cartas/Red_back.jpg")  # Verso da carta
        )

    def move_on_top(self):
        """Move a carta para o topo da pilha."""
        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Retorna a carta à sua posição original."""
        for card in self.draggable_pile:
            card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            card.left = card.slot.left
        self.solitaire.update()

    def place(self, slot):
        """Coloca a carta em um slot."""
        self.draggable_pile = self.get_draggable_pile()
        for card in self.draggable_pile:
            if slot in self.solitaire.tableau:
                card.top = slot.top + len(slot.pile) * CARD_OFFSET
            else:
                card.top = slot.top
            card.left = slot.left

            if card.slot is not None:
                card.slot.pile.remove(card)
            card.slot = slot
            slot.pile.append(card)

        if self.solitaire.check_win():
            self.solitaire.winning_sequence()

        self.solitaire.update()

    def start_drag(self, e: ft.DragStartEvent):
        """Inicia o arrasto da carta."""
        if self.face_up:
            self.draggable_pile = self.get_draggable_pile()
            self.move_on_top()

    def drag(self, e: ft.DragUpdateEvent):
        """Atualiza a posição da carta durante o arrasto."""
        if self.face_up:
            for card in self.draggable_pile:
                card.top = max(0, self.top + e.delta_y) + self.draggable_pile.index(card) * CARD_OFFSET
                card.left = max(0, self.left + e.delta_x)
            self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        """Solta a carta em um slot válido."""
        if self.face_up:
            for slot in self.solitaire.tableau:
                if (
                    abs(self.top - (slot.top + len(slot.pile) * CARD_OFFSET)) < DROP_PROXIMITY
                    and abs(self.left - slot.left) < DROP_PROXIMITY
                ) and self.solitaire.check_tableau_rules(self, slot):
                    self.place(slot)
                    return

            if len(self.draggable_pile) == 1:
                for slot in self.solitaire.foundations:
                    if (
                        abs(self.top - slot.top) < DROP_PROXIMITY
                        and abs(self.left - slot.left) < DROP_PROXIMITY
                    ) and self.solitaire.check_foundations_rules(self, slot):
                        self.place(slot)
                        return

            self.bounce_back()

    def get_draggable_pile(self):
        """Retorna a pilha de cartas que pode ser arrastada."""
        if self.slot and self.slot != self.solitaire.stock and self.slot != self.solitaire.waste:
            return self.slot.pile[self.slot.pile.index(self):]
        return [self]

    def click(self, e):
        """Lida com o clique em uma carta."""
        if self.slot in self.solitaire.tableau:
            if not self.face_up and self == self.slot.get_top_card():
                self.turn_face_up()
        elif self.slot == self.solitaire.stock:
            self.move_on_top()
            self.place(self.solitaire.waste)
            self.turn_face_up()

    def double_click(self, e):
        """Lida com o duplo clique em uma carta."""
        if self.face_up and len(self.get_draggable_pile()) == 1:
            self.move_on_top()
            for slot in self.solitaire.foundations:
                if self.solitaire.check_foundations_rules(self, slot):
                    self.place(slot)
                    return

    def turn_face_up(self):
        """Vira a carta para cima."""
        self.face_up = True
        self.content.content.src = f"cartas/{self.rank.name}{self.suite.name[0].upper()}.jpg"
        if self.page is not None:  # Verifica se a carta está na página
            self.update()

    def turn_face_down(self):
        """Vira a carta para baixo."""
        self.face_up = False
        self.content.content.src = "cartas/Red_back.jpg"
        if self.page is not None:  # Verifica se a carta está na página
            self.update()

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.slots = []
        self.cards = []
        self.stock = None
        self.waste = None
        self.foundations = []
        self.tableau = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    def check_win(self):
        """Verifica se o jogador venceu."""
        return all(len(slot.pile) == 13 for slot in self.foundations)

    def winning_sequence(self):
        """Executa a sequência de vitória."""
        print("Parabéns! Você venceu o jogo!")

    def did_mount(self):
        """Inicializa o jogo após o layout ser montado."""
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        """Cria o baralho de cartas."""
        suites = [
            Suite("C", "BLACK"),
            Suite("D", "RED"),
            Suite("H", "RED"),
            Suite("S", "BLACK"),
        ]
        ranks = [
            Rank("2", 2), Rank("3", 3), Rank("4", 4), Rank("5", 5),
            Rank("6", 6), Rank("7", 7), Rank("8", 8), Rank("9", 9),
            Rank("10", 10), Rank("J", 11), Rank("Q", 12), Rank("K", 13),
            Rank("A", 1)
        ]
        self.cards = [Card(self, suite, rank) for suite in suites for rank in ranks]

    def create_slots(self):
        """Cria os slots do jogo."""
        self.stock = Slot(self, top=0, left=0, border=ft.border.all(1))
        self.waste = Slot(self, top=0, left=100, border=None)
        x = 300
        for _ in range(4):
            self.foundations.append(Slot(self, top=0, left=x, border=ft.border.all(1, "outline")))
            x += 100
        x = 0
        for _ in range(7):
            self.tableau.append(Slot(self, top=150, left=x, border=None))
            x += 100
        self.controls.extend([self.stock, self.waste] + self.foundations + self.tableau)

    def deal_cards(self):
        """Distribui as cartas no tableau."""
        random.shuffle(self.cards)
        remaining_cards = self.cards[:]
        first_slot = 0

        # Distribuir cartas nos slots do tableau
        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                if remaining_cards:
                    top_card = remaining_cards.pop(0)
                    top_card.place(slot)

            first_slot += 1

        # Adicionar todas as cartas restantes ao stock
        for card in remaining_cards:
            card.place(self.stock)

        # Adicionar todas as cartas ao controle principal
        self.controls.extend(self.cards)

        # Forçar a atualização do layout para garantir que as cartas sejam montadas
        self.page.update()  # Certifique-se de que 'self.page' está disponível

        # Virar a última carta de cada slot do tableau para cima
        for slot in self.tableau:
            if slot.pile:
                slot.pile[-1].turn_face_up()

        # Atualizar o layout novamente
        self.update()

    def check_tableau_rules(self, card, slot):
        """Verifica se a carta pode ser movida para o tableau."""
        top_card = slot.get_top_card()
        if top_card:
            return (
                card.suite.color != top_card.suite.color
                and top_card.rank.value - card.rank.value == 1
                and top_card.face_up
            )
        return card.rank.name == "King"

    def check_foundations_rules(self, card, slot):
        """Verifica se a carta pode ser movida para a fundação."""
        top_card = slot.get_top_card()
        if top_card:
            return (
                card.suite.name == top_card.suite.name
                and card.rank.value - top_card.rank.value == 1
            )
        return card.rank.name == "Ace"

def main(page: ft.Page):
    """Função principal para iniciar o jogo."""
    page.title = "Solitaire"
    page.window_width = SOLITAIRE_WIDTH
    page.window_height = SOLITAIRE_HEIGHT
    page.add(Solitaire())

if __name__ == "__main__":
    ft.app(target=main, assets_dir="cartas")