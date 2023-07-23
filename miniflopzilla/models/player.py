import random
from miniflopzilla.aux.utils import CONFIG

class Player:
    def __init__(self):
        self.hand_range = set()
        self.has_range = False

    def add_to_range(self, hand):
        self.hand_range.add(hand)
        self.has_range = True

    def remove_from_range(self, hand):
        self.hand_range.discard(hand)
        self.has_range = self.hand_range is not set()

    def get_random_combo(self):
        hand = random.choice(list(self.hand_range))
        if CONFIG['elements'].index(hand[0]) < CONFIG['elements'].index(hand[0]):
            # suited
            symbol = random.choice(['s','d','h','c'])
            return [ hand[0] + symbol, hand[1] + symbol]
        else:
            # off 
            symbols = random.choice(['ds','sd','ch','cs'])
            return [ hand[0] + symbols[0], hand[1] + symbols[1]]