import flet as ft

CARD_WIDTH = 70
CARD_HEIGHT = 100
DROP_PROXIMITY = 20
CARD_OFFSET = 20

class Card(ft.GestureDetector):
    def __init__(self, solitaire, color):
        super().__init__()
        self.slot = None
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.left = 0  # Inicializa left com 0
        self.top = 0   # Inicializa top com 0
        self.solitaire = solitaire
        self.color = color
        self.content = ft.Container(bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGHT)
        self.draggable_pile = []

    def move_on_top(self):
        """Moves draggable card to the top of the stack"""
        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Returns card to its original position"""
        for card in self.draggable_pile:
            card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            card.left = card.slot.left
        self.solitaire.update()

    def place(self, slot):
        """Place card to the slot"""
        for card in self.draggable_pile:
            card.top = slot.top + len(slot.pile) * CARD_OFFSET
            card.left = slot.left

            if card.slot is not None:
                card.slot.pile.remove(card)

            card.slot = slot
            slot.pile.append(card)
        self.solitaire.update()

    def start_drag(self, e: ft.DragStartEvent):
        self.draggable_pile = self.get_draggable_pile()
        self.move_on_top()
        self.update()

    def drag(self, e: ft.DragUpdateEvent):
        for card in self.draggable_pile:
            card.top = max(0, self.top + e.delta_y) + self.draggable_pile.index(card) * CARD_OFFSET
            card.left = max(0, self.left + e.delta_x)
        self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if abs(self.top - slot.top) < DROP_PROXIMITY and abs(self.left - slot.left) < DROP_PROXIMITY:
                self.place(slot)
                return
        self.bounce_back()

    def get_draggable_pile(self):
        """Returns list of cards that will be dragged together, starting with the current card"""
        if self.slot is not None:
            return self.slot.pile[self.slot.pile.index(self):]
        return [self]

class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.pile = []
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.left = left
        self.top = top
        self.border = ft.border.all(1)

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.slots = []
        self.cards = []
        self.width = 1000
        self.height = 500

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        card1 = Card(self, color="GREEN")
        card2 = Card(self, color="YELLOW")
        self.cards = [card1, card2]

    def create_slots(self):
        self.slots.append(Slot(top=0, left=0))
        self.slots.append(Slot(top=0, left=200))
        self.slots.append(Slot(top=0, left=300))
        self.controls.extend(self.slots)
        self.update()

    def deal_cards(self):
        self.controls.extend(self.cards)
        for card in self.cards:
            card.place(self.slots[0])
        self.update()

def main(page: ft.Page):
    solitaire = Solitaire()
    page.add(solitaire)

ft.app(target=main, assets_dir="images")