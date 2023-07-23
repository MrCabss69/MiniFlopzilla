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
        if self.current_player == 1:
            for i, player in enumerate(self.players, start=1):
                combo = player.get_random_combo()
                self.table.add_to_hand(i, list(combo))
            self.grid.reset()
            results = self.table.simulate()
            return results
        else:
            return None
    
    def are_all_ranges_set(self):
        return all(player.has_range for player in self.players)
    
    def is_p1_range_set(self):
        return self.players[0].has_range
    
    def reset(self):
        self.grid = Grid()
        self.players = [Player(), Player()]
        self.current_player = 0
        self.table = HoldemTable(num_players=2, deck_type='full')