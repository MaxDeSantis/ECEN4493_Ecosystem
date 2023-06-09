import GeneticCode
from GeneticCode import GeneticCode

import SimulationParameters

from Animal import Animal

class Herbivore (Animal):
    def __init__(self, energy_value, sim_params: SimulationParameters, genetic_code: GeneticCode, manager, random_instance, generation=0):
        super().__init__(energy_value, sim_params, genetic_code, manager, random_instance, generation)
        
        self.speed = 4
        self.act_range = self.params.herbivore_act_range
        self.flee_range = 4 * self.act_range