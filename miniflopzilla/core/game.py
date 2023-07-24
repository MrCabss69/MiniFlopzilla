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
        self.grid.toggle_cell(
            mouse_position, self.players[self.current_player])

    def start_simulation(self):
        
        if self.current_player == 1:
            results = {}
            for combo1 in self.players[0].get_all_combos():
                for combo2 in self.players[1].get_all_combos():
                    if len(set(combo1).intersection(set(combo2))) == 0:
                        self.table = HoldemTable(num_players=2, deck_type='full')
                        self.table.add_to_hand(1, list(combo1))
                        self.table.add_to_hand(2, list(combo2))
                        result = self.table.simulate()
                        for key, value in result.items():
                            if key not in results:
                                results[key] = 0
                            results[key] += value
            total = sum(results.values())
            for key in results:
                results[key] /= total

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
