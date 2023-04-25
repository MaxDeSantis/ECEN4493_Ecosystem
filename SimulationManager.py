
# Spawn the plants
# Spawn the herbivores
# Tick the herbivores one after the other

import Plant
from Plant import Plant

import random

import Utility

class SimulationManager:
    def __init__(self, num_plants, num_herbivores):
        self.num_plants = num_plants
        self.num_herbivores = num_herbivores
        self.plants = []
        
        random.seed(5)
        self.rand_instance = random.Random()
        
        self.x_min = -50
        self.x_max = 50
        self.y_min = -50
        self.y_max = 50
        
        print("SimulationManager initialized")
        self.generate_initial_herbivores()
        
    
    def generate_initial_plants(self):
        print("Generating initial plants")
        
        for i in range(self.num_plants):
            newPlant = Plant(Utility.random_position(self.rand_instance, self.x_min, self.x_max, self.y_min, self.y_max))
            self.plants.append(newPlant)
    
    def generate_initial_herbivores(self):
        pass
    
    
    def run_simulation(self):
        pass



















def main():
    sim_manager = SimulationManager()
    
    sim_manager.run_simulation()


if __name__ == "__main__":
    main()