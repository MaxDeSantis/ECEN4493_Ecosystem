
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from SimulationParameters import SimulationParameters

import pygame

class SimVisualizer:
    def __init__(self, params:SimulationParameters):
        self.params = params
        
        pygame.init()
        self.size = self.width, self.height = self.params.x_max - self.params.x_min, self.params.y_max - self.params.y_min
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Herbivore Simulation')
        
        self.WHITE = (255,255,255)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        self.screen.fill(self.WHITE)
        
    def draw_state(self, herbivores,carnivores, plants):
        
        self.screen.fill(self.WHITE)
        for p in plants:
            pygame.draw.circle(self.screen, self.GREEN, (p.position.x + self.center_x, p.position.y + self.center_y), 5)
            
        for h in herbivores:
            pygame.draw.circle(self.screen, self.BLUE, (h.position.x + self.center_x, h.position.y + self.center_y), 5)
            
        for c in carnivores:
            pygame.draw.circle(self.screen, self.RED, (c.position.x + self.center_x, c.position.y + self.center_y), 5)
            
        pygame.display.flip()
    