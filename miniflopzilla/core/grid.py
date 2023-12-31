import pygame
import numpy as np
from miniflopzilla.aux.utils import CONFIG


class Grid:
    def __init__(self):
        self.grid = np.zeros((CONFIG["n"], CONFIG["n"]))
        self.vals = np.zeros((CONFIG["n"], CONFIG["n"]))

    def draw(self, ventana):
        for i in range(CONFIG["n"]):
            for j in range(CONFIG["n"]):
                pygame.draw.rect(ventana, CONFIG["colors"][int(self.vals[i][j])], (j*CONFIG["cell_size"], i*CONFIG["cell_size"], CONFIG["cell_size"], CONFIG["cell_size"]))

        # Add labels to rows and columns
        label_font = pygame.font.SysFont(CONFIG["label_font"], CONFIG["label_size"])
        for i in range(len(CONFIG["elements"])):
            label = label_font.render(CONFIG["elements"][i], True, pygame.Color(CONFIG["label_color"]))
            label_rect = label.get_rect(center=((i+1)*CONFIG["cell_size"]+CONFIG["cell_size"]//2, CONFIG["cell_size"]//2))
            ventana.blit(label, label_rect)
            label_rect = label.get_rect(center=(CONFIG["cell_size"]//2, (i+1)*CONFIG["cell_size"]+CONFIG["cell_size"]//2))
            ventana.blit(label, label_rect)

        for i in range(CONFIG["n"] + 1):
            pygame.draw.line(ventana, (250, 250, 250), [i*CONFIG["cell_size"], 0], [i*CONFIG["cell_size"], CONFIG["n"]*CONFIG["cell_size"]]) 
            pygame.draw.line(ventana, (250, 250, 250), [0, i*CONFIG["cell_size"]], [CONFIG["n"]*CONFIG["cell_size"], i*CONFIG["cell_size"]]) 

    def toggle_cell(self, mouse_position, player):
        x, y = mouse_position
        i, j = y // CONFIG["cell_size"], x // CONFIG["cell_size"]
        if 0 < i < CONFIG["n"] and 0 < j < CONFIG["n"]:  # Do not allow selection of the label cells and check if indices are within range
            hand = CONFIG["elements"][i-1] + CONFIG["elements"][j-1]  # Subtract 1 from the indices to get the correct element
            if self.vals[i][j] == 1:
                self.vals[i][j] = 0
                player.remove_from_range(hand)
            else:
                self.vals[i][j] = 1
                player.add_to_range(hand)

    def reset(self):
        self.vals = np.zeros((CONFIG["n"], CONFIG["n"]))
