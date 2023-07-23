from miniflopzilla.core.grid import Grid
from miniflopzilla.models.player import Player
from miniflopzilla.models.table import HoldemTable


class Game:
    def __init__(self):
        self.grid = Grid()
        self.players = [Player(), Player()]
        self.current_player = 0
        self.table = HoldemTable(num_players=2, deck_type='full')

    def update_player_range(self, mouse_position):
        self.grid.toggle_cell(mouse_position, self.players[self.current_player])

    def start_simulation(self):
        self.grid.reset()
        if self.current_player == 1:
            for i, player in enumerate(self.players, start=1):
                combo = player.get_random_combo()
                self.table.add_to_hand(i, list(combo))
            results = self.table.simulate()
            self.current_player = 0
            return results
        else:
            self.current_player = 1
            return None