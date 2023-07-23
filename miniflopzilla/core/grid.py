import pygame
from pygame_widgets.button import Button
from table import HoldemTable
import numpy as np
import random

# Constantes y configuración global
CONFIG = {
    "n": 14,
    "cell_size": 35,
    "colors": [(23, 63, 53), (0, 255, 153)],
    "elements": ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'],
    "label_color": "Coral",
    "label_font": "arial",
    "label_size": 20,
}

class Player:
    def __init__(self):
        self.hand_range = set()

    def add_to_range(self, hand):
        self.hand_range.add(hand)

    def remove_from_range(self, hand):
        self.hand_range.discard(hand)

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

class Grid:
    def __init__(self):
        self.grid = np.zeros((CONFIG["n"], CONFIG["n"]))
        self.vals = np.zeros((CONFIG["n"], CONFIG["n"]))

    def draw(self, ventana):
        for i in range(CONFIG["n"]):
            for j in range(CONFIG["n"]):
                pygame.draw.rect(ventana, CONFIG["colors"][int(self.vals[i][j])], (j*CONFIG["cell_size"], i*CONFIG["cell_size"], CONFIG["cell_size"], CONFIG["cell_size"]))
        for i in range(1, CONFIG["n"] + 1):
            pygame.draw.line(ventana, (250, 250, 250), [i*CONFIG["cell_size"], 0], [i*CONFIG["cell_size"], CONFIG["n"]*CONFIG["cell_size"]]) 
            pygame.draw.line(ventana, (250, 250, 250), [0, i*CONFIG["cell_size"]], [CONFIG["n"]*CONFIG["cell_size"], i*CONFIG["cell_size"]]) 

    def toggle_cell(self, mouse_position, player):
        x, y = mouse_position
        i, j = y // CONFIG["cell_size"], x // CONFIG["cell_size"]
        hand = CONFIG["elements"][i] + CONFIG["elements"][j]
        if self.vals[i][j] == 1:
            self.vals[i][j] = 0
            player.remove_from_range(hand)
        else:
            self.vals[i][j] = 1
            player.add_to_range(hand)

    def reset(self):
        self.vals = np.zeros((CONFIG["n"], CONFIG["n"]))

class Window:
    def __init__(self) -> None:
        self.shape = (CONFIG["n"]*CONFIG["cell_size"], CONFIG["n"]*CONFIG["cell_size"]+75)
        self.ventana = pygame.display.set_mode(self.shape)
        pygame.display.set_caption("MiniFlopzilla")
        self.button = Button(
            self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p1 Range',
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=self.show_results
        )
        self.grid = Grid()
        self.players = [Player(), Player()]
        self.current_player = 0
        self.table = HoldemTable(num_players=2, deck_type='full')

    def draw(self):
        self.grid.draw(self.ventana)
        self.button.draw()
        
    def show_simulation_results(self, results):
        # Limpiar la ventana antes de dibujar los resultados
        self.ventana.fill((0, 0, 0))

        # Crear una superficie de texto con los resultados
        font = pygame.font.Font(None, 25)
        text = font.render(str(results), True, (255, 255, 255)) 

        # Dibujar la superficie de texto en la ventana
        self.ventana.blit(text, (50, 50))  

        # Actualizar la ventana para mostrar los resultados
        pygame.display.update() 

        # Esperar antes de continuar
        pygame.time.wait(50000)  # Esperar 5 segundos

        # Aquí puedes cargar la siguiente pantalla (por ejemplo, la pantalla principal)
        self.main()
        
    def show_results(self):
        self.grid.reset()
        if self.current_player == 1:
            for i, player in enumerate(self.players, start=1):
                combo = player.get_random_combo()
                self.table.add_to_hand(i, list(combo))
            results = self.table.simulate()
            self.show_simulation_results(results)
            self.button = Button(
            self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p1 Range',
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=self.show_results
        )
            self.current_player = 0
        else:
            self.button = Button(
            self.ventana, ((CONFIG["n"]*CONFIG["cell_size"])/2)-50, (CONFIG["n"]*CONFIG["cell_size"])+15, 100, 50, text='Set p2 Range',
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=self.show_results
        )
            self.current_player = 1


    def main(self): 
        pygame.init()
        pygame.font.init()
        while True:
            self.draw()
            pygame.display.update()

            for event in pygame.event.get():
                self.button.listen(event)
                if event.type == pygame.QUIT:
                    pygame.display.update()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[1] > CONFIG["n"]*CONFIG["cell_size"]:
                        self.button.listen(event)
                        self.show_results()
                    else:
                        self.grid.toggle_cell(pygame.mouse.get_pos(), self.players[self.current_player])
                        self.draw()
                    pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    window = Window()
    window.main()
