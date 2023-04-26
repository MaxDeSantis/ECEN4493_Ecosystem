
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from SimulationParameters import SimulationParameters

import pygame
from pygame.locals import *

class SimVisualizer:
    def __init__(self, params:SimulationParameters):
        self.params = params
        
        pygame.init()
        self.size = self.width, self.height = self.params.x_max - self.params.x_min, self.params.y_max - self.params.y_min
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Ecosystem Simulation')
        
        self.WHITE = (255,255,255)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        #self.screen.fill(self.WHITE)
        
        self.background = pygame.Surface(self.screen.get_size())
        
        self.font = pygame.font.SysFont("monospace", 30)
        
        
    def draw_state(self, epoch, herbivores,carnivores, plants):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #self.screen.fill(self.WHITE)
        pygame.draw.rect(self.background, self.WHITE, (0,0,self.width,self.height))

        #self.screen.draw
        for p in plants:
            #pygame.draw.circle(self.screen, self.GREEN, (p.position.x + self.center_x, p.position.y + self.center_y), 5)
            pygame.draw.circle(self.background, self.GREEN, (p.position.x + self.center_x, p.position.y + self.center_y), 5)
        for h in herbivores:
            pygame.draw.circle(self.background, self.BLUE, (h.position.x + self.center_x, h.position.y + self.center_y), 5)
            
        for c in carnivores:
            pygame.draw.circle(self.background, self.RED, (c.position.x + self.center_x, c.position.y + self.center_y), 5)
        
        e_text = self.font.render("N: " + str(epoch), 1, (0,0,0))
        h_text = self.font.render("H: " + str(len(herbivores)), 1, (0,0,0))
        c_text = self.font.render("C: " + str(len(carnivores)), 1, (0,0,0))
        
        e_text_rect = e_text.get_rect()
        h_text_rect = h_text.get_rect()
        c_text_rect = c_text.get_rect()
        
        e_text_rect.center = (self.width - 50, 20)
        h_text_rect.center = (self.width - 50, 40)
        c_text_rect.center = (self.width - 50, 60)
        self.background.blit(e_text, e_text_rect)
        self.background.blit(h_text, h_text_rect)
        self.background.blit(c_text, c_text_rect)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
    