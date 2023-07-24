import pygame
import numpy as np
from pygame_widgets.button import Button
from miniflopzilla.models.table import HoldemTable
from miniflopzilla.aux.utils import CONFIG
from miniflopzilla.core.game import Game
import threading
import time


class UIController:
    def __init__(self, game) -> None:
        self.shape = (CONFIG["n"]*CONFIG["cell_size"],
                      CONFIG["n"]*CONFIG["cell_size"]+75)
        self.ventana = pygame.display.set_mode(self.shape)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("MiniFlopzilla")

        self.game = game
        self.create_button('Set p1 Range')

    def create_button(self, text):
        self.button = Button(
            self.ventana, (self.shape[0]//2)-50, self.shape[1]-60, 100, 50, text=text,
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10)

    def draw(self):
        self.ventana.fill((0, 0, 0))
        self.game.grid.draw(self.ventana)
        self.button.draw()

    def update_display(self):
        self.draw()
        pygame.display.update()

    def show_loading_animation(self):
        image = pygame.image.load('loading.png')

        # Calcula las coordenadas para centrar la imagen rotada
        x = (self.shape[0] - image.get_width()) // 2
        y = (self.shape[1] - image.get_height()) // 2

        # Muestra la imagen rotada
        self.ventana.fill((255, 255, 255))
        self.ventana.blit(image, (x, y))
        pygame.display.update()
        
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

class GameController:
    def __init__(self, game, ui_controller) -> None:
        self.game = game
        self.ui_controller = ui_controller
        self.simulation_running = False

    def start_simulation(self):
        results = self.game.start_simulation()
        self.simulation_running = False
        return results

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_y = pygame.mouse.get_pos()[1]
            if mouse_y > CONFIG["n"]*CONFIG["cell_size"]:
                self.game.grid.reset()
                if not self.game.players[self.game.current_player].has_range:
                    print("Player must set range before starting simulation")
                elif self.game.current_player == 1:
                    self.ui_controller.show_loading_animation()
                    results = self.start_simulation()
                    self.ui_controller.show_simulation_results(
                        results) if results else self.ui_controller.create_button('Set p1 Range')
                else:
                    self.ui_controller.create_button(f'Set p2 Range')
                    self.game.current_player = (
                        self.game.current_player + 1) % len(self.game.players)
            else:
                self.game.update_player_range(pygame.mouse.get_pos())
            self.ui_controller.update_display()

    def main(self):
        pygame.init()
        pygame.font.init()
        while True:
            self.ui_controller.update_display()
            for event in pygame.event.get():
                self.handle_event(event)
