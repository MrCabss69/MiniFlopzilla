from miniflopzilla.core.game import Game
from miniflopzilla.core.controllers import UIController, GameController

if __name__ == "__main__":
    game = Game()
    ui_controller = UIController(game)
    game_controller = GameController(game, ui_controller)
    game_controller.main()
