

import GeneticCode
from GeneticCode import GeneticCode

import Utility
from Utility import Position

import SimulationParameters

from Animal import Animal

class Carnivore (Animal):
    def __init__(self, energy_value, sim_params: SimulationParameters, genetic_code: GeneticCode, manager, random_instance, generation=0):
        super().__init__(energy_value, sim_params, genetic_code, manager, random_instance, generation)
        
        self.speed = 5
        self.act_range = self.params.carnivore_act_range