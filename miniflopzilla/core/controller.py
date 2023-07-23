import pygame
import numpy as np
from pygame_widgets.button import Button
from miniflopzilla.models.table import HoldemTable
from miniflopzilla.aux.utils import CONFIG
from miniflopzilla.core.game import Game

class Controller:
    def __init__(self, game) -> None:
        self.shape = (CONFIG["n"]*CONFIG["cell_size"], CONFIG["n"]*CONFIG["cell_size"]+75)
        self.ventana = pygame.display.set_mode(self.shape)
        pygame.display.set_caption("MiniFlopzilla")
        self.game = game
        self.create_button('Set p1 Range')

    def create_button(self, text):
        self.button = Button(
            self.ventana, (self.shape[0]//2)-50, self.shape[1]-60, 100, 50, text=text,
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=self.start_simulation
        )

    def draw(self):
        self.ventana.fill((0, 0, 0))
        self.game.grid.draw(self.ventana)
        self.button.draw()

    def show_simulation_results(self, results):
        self.ventana.fill((0, 0, 0))
        font = pygame.font.Font(None, 25)
        y_offset = 50
        for i, player in enumerate(self.game.players):
            text = font.render(f"Player {i+1} Range: {player.hand_range}", True, (255, 255, 255))
            self.ventana.blit(text, (50, y_offset))
            y_offset += 30

        for key, value in results.items():
            text = font.render(f"{key}: {value}", True, (255, 255, 255))
            self.ventana.blit(text, (50, y_offset))
            y_offset += 30

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
        self.game.reset()
        self.main()

    def start_simulation(self):
        if not self.game.are_all_ranges_set():
            next_player = 'p2' if self.game.is_p1_range_set() else 'p1'
            self.create_button(f'Set {next_player} Range')
        else:
            self.show_loading_animation()
            results = self.game.start_simulation()
            self.show_simulation_results(results) if results else self.create_button('Set p1 Range')

    def show_loading_animation(self):
        self.ventana.fill((0, 0, 0))
        loading_animation = pygame.image.load('loading.png')
        self.ventana.blit(loading_animation,
                          (self.shape[0]//2, self.shape[1]//2))
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_y = pygame.mouse.get_pos()[1]
            if mouse_y > CONFIG["n"]*CONFIG["cell_size"]:
                if self.game.players[self.game.current_player].has_range:
                    results = self.start_simulation()
                    print(results)
                else:
                    print("Player must set range before starting simulation")
                self.game.grid.reset()
                self.game.current_player = (self.game.current_player + 1) % len(self.game.players)
            else:
                self.game.update_player_range(pygame.mouse.get_pos())
            self.draw()
            pygame.display.update()

    def main(self):
        pygame.init()
        pygame.font.init()
        while True:
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_event(event)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    game = Game()
    controller = Controller(game)
    controller.main()
