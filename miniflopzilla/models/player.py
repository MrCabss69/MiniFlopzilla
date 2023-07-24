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

    def get_random_combo(self,range=None):
        if range is None:
            range = self.hand_range
        else:
            range = range
        hand = random.choice(list(range))
        if CONFIG['elements'].index(hand[0]) < CONFIG['elements'].index(hand[0]):
            # suited
            symbol = random.choice(['s','d','h','c'])
            return [ hand[0] + symbol, hand[1] + symbol]
        else:
            # off 
            symbols = random.choice(['ds','sd','ch','cs'])
            return [ hand[0] + symbols[0], hand[1] + symbols[1]]
        
    def get_all_combos(self):
        all_combos = []
        for hand in list(self.hand_range):
            if CONFIG['elements'].index(hand[0]) < CONFIG['elements'].index(hand[1]):
                # suited
                symbols = ['s','d','h','c']
                combos = []
                for symbol in symbols:
                    combos.append([hand[0] + symbol, hand[1] + symbol])
                all_combos.append(random.choice(combos))
            else:
                # off 
                symbols = ['ds','sd','ch','cs']
                combos =  []
                for symbol in symbols:
                    combos.append([hand[0] + symbol[0], hand[1] + symbol[1]])
                all_combos.append(random.choice(combos))
        return all_combos