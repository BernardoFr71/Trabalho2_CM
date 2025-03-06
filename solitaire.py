from card import Card
from slot import Slot
import random
import flet as ft
import json
import time
import threading

class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color

class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value

class Solitaire(ft.Stack):
    def __init__(self, settings, on_win):
        super().__init__()
        self.history = []  # Lista para armazenar os estados do jogo
        self.settings = settings
        self.timer_running = False
        self.time_remaining = 300  # 5 minutos em segundos
        self.timer_text = None  # Referência ao texto do temporizador
        self.timer_thread = None
        self.score = 0
        self.score_text = None  # Referência ao texto da pontuação
        self.width = 1000
        self.height = 500
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def update_card_backs(self):
        """Atualiza as costas das cartas com base nas configurações."""
        for card in self.cards:
            if not card.face_up:  # Apenas atualiza as cartas viradas para baixo
                card.content.content.src = self.settings.card_back
        self.update()  # Atualiza a interface

    def start_timer(self):
        """Inicia o temporizador em uma thread separada."""
        if self.timer_thread and self.timer_thread.is_alive():
            return  # Evita iniciar múltiplos temporizadores

        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

    def run_timer(self):
        """Executa o temporizador."""
        while self.timer_running and self.time_remaining > 0:
            time.sleep(1)
            self.time_remaining -= 1
            self.update_timer_display()  # Atualiza o display do temporizador
            if self.time_remaining == 0:
                self.on_timeout()
                break

    def update_timer_display(self):
        """Atualiza o display do temporizador."""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        if self.timer_text:
            self.timer_text.value = f"Tempo: {minutes:02}:{seconds:02}"
            self.update()  # Atualiza a interface

    def update_score(self, points):
        """Atualiza a pontuação."""
        self.score += points
        if self.score_text:
            self.score_text.value = f"Pontuação: {self.score}"
            self.update()  # Atualiza a interface

    def on_win(self):
        """Calcula a pontuação final ao vencer."""
        time_bonus = self.time_remaining * 10  # Bônus por tempo restante
        self.update_score(time_bonus)
        print(f"Você venceu! Pontuação final: {self.score}")
        self.stop_timer()  # Para o temporizador ao vencer

    def save_state(self):
        """Salva o estado atual do jogo."""
        state = {
            "stock": [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in self.stock.pile],
            "waste": [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in self.waste.pile],
            "foundation": [
                [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in slot.pile]
                for slot in self.foundation
            ],
            "tableau": [
                [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in slot.pile]
                for slot in self.tableau
            ],
        }
        self.history.append(state)

    def restore_state(self, state):
        """Restaura o jogo para um estado específico."""
        # Limpa todos os slots
        self.stock.pile.clear()
        self.waste.pile.clear()
        for slot in self.foundation:
            slot.pile.clear()
        for slot in self.tableau:
            slot.pile.clear()

        # Mapeia as cartas do jogo atual para facilitar a busca
        card_map = {f"{card.rank.name}_{card.suite.name}": card for card in self.cards}

        # Função auxiliar para processar cada carta
        def process_card(card_data, slot):
            if isinstance(card_data, list) and len(card_data) == 2:  # Novo formato: [card_name, face_up]
                card_name, face_up = card_data
            else:  # Formato antigo: apenas card_name
                card_name = card_data
                face_up = False  # Assume que a carta estava virada para baixo

            card = card_map[card_name]
            card.slot = None  # Limpa o slot atual da carta
            card.place(slot)
            if face_up:
                card.turn_face_up()
            else:
                card.turn_face_down()

        # Restaura o stock
        for card_data in state["stock"]:
            process_card(card_data, self.stock)

        # Restaura o waste
        for card_data in state["waste"]:
            process_card(card_data, self.waste)

        # Restaura as fundações
        for i, foundation_pile in enumerate(state["foundation"]):
            for card_data in foundation_pile:
                process_card(card_data, self.foundation[i])

        # Restaura o tableau
        for i, tableau_pile in enumerate(state["tableau"]):
            for card_data in tableau_pile:
                process_card(card_data, self.tableau[i])

        # Atualiza a interface
        self.update()

    def save_game(self, filename="saved_game.json"):
        """Salva o estado atual do jogo em um arquivo JSON."""
        state = {
            "stock": [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in self.stock.pile],
            "waste": [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in self.waste.pile],
            "foundation": [
                [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in slot.pile]
                for slot in self.foundation
            ],
            "tableau": [
                [[f"{card.rank.name}_{card.suite.name}", card.face_up] for card in slot.pile]
                for slot in self.tableau
            ],
        }
        with open(filename, "w") as file:
            json.dump(state, file)

    def load_game(self, filename="saved_game.json"):
        """Carrega o estado do jogo de um arquivo JSON."""
        with open(filename, "r") as file:
            state = json.load(file)
        self.restore_state(state)
        self.update()

    def undo(self):
        """Desfaz a última jogada."""
        if len(self.history) > 1:
            print(f"Desfazendo jogada. Histórico: {len(self.history)} estados.")
            self.history.pop()  # Remove o estado atual
            previous_state = self.history[-1]  # Pega o estado anterior
            self.restore_state(previous_state)
            self.update()
        else:
            print("Nada para desfazer. Histórico vazio.")
        
    def create_slots(self):
        # Stock (baralho)
        self.stock = Slot(
            solitaire=self, slot_type="stock", top=20, left=20, border=ft.border.all(1)
        )

        # Waste (descarte)
        self.waste = Slot(
            solitaire=self, slot_type="waste", top=20, left=120, border=None
        )

        # Foundation (fundações)
        self.foundation = []
        x = 320  # Posição inicial das fundações
        for i in range(4):
            self.foundation.append(
                Slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=20,
                    left=x,
                    border=ft.border.all(1, "outline"),
                )
            )
            x += 100  # Espaçamento entre as fundações

        # Tableau (tableau)
        self.tableau = []
        x = 20  # Posição inicial do tableau
        for i in range(7):
            self.tableau.append(
                Slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=150,  # Posição vertical do tableau
                    left=x,
                    border=None
                )
            )
            x += 100  # Espaçamento entre as colunas do tableau

        # Adiciona os slots à interface
        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                file_name = f"{rank.name}_{suite.name}.svg"
                #print(file_name)
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))
        # self.stock = self.cards
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        # Tableau
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        # Reveal top cards in slot piles:
        for number in range(len(self.tableau)):
            #self.tableau[number].pile[-1].turn_face_up()
            self.tableau[number].get_top_card().turn_face_up()

        # Stock pile
        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)

    def move_on_top(self, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()


    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def display_waste(self):
        if self.settings.waste_size == 3:
            self.waste.fan_top_three()
        self.update()

    def restart_stock(self):
        self.waste.pile.reverse()
        while len(self.waste.pile) > 0:
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
        self.update()

    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.name == top_card.suite.name
                and current_card.rank.value - top_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.color != top_card.suite.color
                and top_card.rank.value - current_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "King"

    def check_if_you_won(self):
        cards_num = 0
        for slot in self.foundation:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False