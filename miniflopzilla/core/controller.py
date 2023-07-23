import pygame
import numpy as np
from pygame_widgets.button import Button
from miniflopzilla.models.table import HoldemTable
from miniflopzilla.aux.utils import CONFIG
from miniflopzilla.core.game import Game


class Controller:
    def __init__(self, game) -> None:
        self.shape = (CONFIG["n"]*CONFIG["cell_size"],
                      CONFIG["n"]*CONFIG["cell_size"]+75)
        self.ventana = pygame.display.set_mode(self.shape)
        pygame.display.set_caption("MiniFlopzilla")
        self.button = Button(
            self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p1 Range',
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=self.start_simulation
        )
        self.game = game

    def draw(self):
        self.game.grid.draw(self.ventana)
        self.button.draw()

    def show_simulation_results(self, results):
        # Limpiar la ventana antes de dibujar los resultados
        self.ventana.fill((0, 0, 0))
        font = pygame.font.Font(None, 25)
        text = font.render(str(results), True, (255, 255, 255))
        self.ventana.blit(text, (50, 50))
        pygame.display.update()
        pygame.time.wait(50000)
        self.main()

    def start_simulation(self):
        results = self.game.start_simulation()
        if results is not None:
            self.show_simulation_results(results)
            self.button = Button(
                self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p1 Range',
                fontSize=20, margin=10, inactiveColour=(255, 0, 0),
                pressedColour=(0, 255, 0), radius=10, onClick=self.start_simulation
            )
        else:
            self.button = Button(
                self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p2 Range',
                fontSize=20, margin=10, inactiveColour=(255, 0, 0),
                pressedColour=(0, 255, 0), radius=10, onClick=self.start_simulation
            )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[1] > CONFIG["n"]*CONFIG["cell_size"]:
                self.start_simulation()
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
