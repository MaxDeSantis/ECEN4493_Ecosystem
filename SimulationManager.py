
# Spawn the plants
# Spawn the herbivores
# Tick the herbivores one after the other

import Plant
from Plant import Plant

import Herbivore
from Herbivore import Herbivore

import random
import time

import Utility

from Element import Element
import math
import GeneticCode as gc
from GeneticCode import GeneticCode

import SimulationParameters
from SimulationParameters import SimulationParameters
import numpy as np
from SimVisualizer import SimVisualizer

import matplotlib.pyplot as plt

from Carnivore import Carnivore
import Animal

class SimulationManager:
    def __init__(self):

        self.plants = []
        self.herbivores = []
        self.carnivores = []
        
        self.epoch_count = 0
        
        self.best_herbivores = []
        self.best_carnivores = []
        
        self.plant_count = 0
        self.herbivore_count = 0
        self.carnivore_count = 0
        
        random.seed(5)
        self.rand_instance = random.Random()
        self.sim_iteration = 0
        self.params = SimulationParameters()
        
        self.vis = SimVisualizer(self.params)
        
        # self.herbivore_data_file = open(self.params.herb_data_file, 'w')
        # self.plant_data_file = open(self.params.plant_data_file, 'w')
        
        self.num_best_herbi = math.ceil(self.params.mutation_percentage * self.params.num_herbivores)
        self.num_best_carni = math.ceil(self.params.mutation_percentage * self.params.num_carnivores)
                
        print("SimulationManager initialized")
        self.generate_initial_plants()
        self.generate_initial_herbivores()
        self.generate_initial_carnivores()
        
        self.sim_data = np.zeros((self.params.sim_epochs, self.params.simulation_duration, 3))
        
        
        
        
    def print_sim_status(self):
        print(f'Iteration: {self.sim_iteration}, Plants: {self.plant_count}, Herbivores: {self.herbivore_count}, Carnivores: {self.carnivore_count}')
        
    def update_sim_status(self):        
        self.sim_data[self.epoch_count, self.sim_iteration, 0] = self.plant_count #len(self.plants)
        self.sim_data[self.epoch_count, self.sim_iteration, 1] = self.herbivore_count #len(self.herbivores)
        self.sim_data[self.epoch_count, self.sim_iteration, 2] = self.carnivore_count #len(self.carnivores)
        
    
    def plot_sim_results(self):
        fig, ax = plt.subplots()
        
        # graph sim data
        x = np.arange(self.params.simulation_duration)
        ax.plot(x, self.sim_data[:,:,0], label='Plants')
        ax.plot(x, self.sim_data[:,:,1], label='Herbivores')
        ax.plot(x, self.sim_data[:,:,2], label='Carnivores')
        
        ax.set_xlabel('Simulation Iteration')
        ax.set_ylabel('Number of Plants/Herbivores/Carnivores')
        
        ax.legend()
        plt.show()
        
    def generate_initial_plants(self):
        print(f'Generating {self.params.num_plants} initial plants')
        
        for i in range(self.params.num_plants):
            new_plant = Plant(Utility.random_position(self.rand_instance, self.params), self.params.plant_energy_value)
            self.plants.append(new_plant)
        self.plant_count = len(self.plants)
    
    def generate_initial_herbivores(self):
        
        print(f'Generating {self.params.num_herbivores} initial herbivores')

        for i in range(self.params.num_herbivores):
            new_herbi = Herbivore(self.params.herbivore_energy_value, self.params, GeneticCode(), self, self.rand_instance, 0)
            self.herbivores.append(new_herbi)
        self.herbivore_count = len(self.herbivores)
            
    def generate_initial_carnivores(self):
        
        print(f'Generating {self.params.num_carnivores} initial carnivores')

        for i in range(self.params.num_carnivores):
            new_carni = Carnivore(self.params.herbivore_energy_value, self.params, GeneticCode(), self, self.rand_instance, 0)
            self.carnivores.append(new_carni)
        self.carnivore_count = len(self.carnivores)
        
    def generate_mutated_animals(self):
        herbi_mutations = int(self.params.num_herbivores / self.num_best_herbi)
        carni_mutations = int(self.params.num_carnivores / self.num_best_carni)
        
        self.herbivores.clear()
        self.herbivore_count = 0
        for i in range(self.num_best_herbi):
            for j in range(herbi_mutations):
                new_genome = gc.mutate(self.best_herbivores[i].genes, self.params.mutation_percentage)
                new_herbi = Herbivore(self.params.herbivore_energy_value, self.params, new_genome, self, self.rand_instance, 0)
                self.herbivores.append(new_herbi)
        
        for i in range(self.num_best_carni):
            for j in range(carni_mutations):
                new_genome = gc.mutate(self.best_carnivores[i].genes, self.params.mutation_percentage)
                new_carni = Carnivore(self.params.herbivore_energy_value, self.params, new_genome, self, self.rand_instance, 0)
                self.carnivores.append(new_carni)
        
        self.herbivore_count = len(self.herbivores)
        self.carnivore_count = len(self.carnivores)
        
        print(f'Generated {self.herbivore_count} mutated herbivores')
        print(f'Generated {self.carnivore_count} mutated carnivores')

    def update_plants(self):
        # Spawn new plants randomly
        new_plant_count = self.rand_instance.randint(0, self.params.plant_spawn_count_max)
        for i in range(new_plant_count):     
            if self.rand_instance.random() < self.params.plant_spawn_probability:
                new_plant = Plant(Utility.random_position(self.rand_instance, self.params), self.params.plant_energy_value)
                self.plants.append(new_plant)
                self.plant_count += 1
            
    def update_herbivores(self):

        for herbi in self.herbivores:
            herbi.SIM_update()
            
    def update_carnivores(self):
        for carni in self.carnivores:
            carni.SIM_update()

            
    def breed_animals(self, animal1:Animal, animal2:Animal):
        new_genes = gc.crossover(animal1.genes, animal2.genes)
        new_generation = max(animal1.generation, animal2.generation) + 1
        if isinstance(animal1, Herbivore):
            if self.herbivore_count >= self.params.max_herbivores:
                return
            baby_herbi = Herbivore(self.params.herbivore_energy_value, self.params, new_genes, self, self.rand_instance, new_generation)
            self.herbivores.append(baby_herbi)
            self.herbivore_count += 1
        elif isinstance(animal1, Carnivore):
            if self.carnivore_count >= self.params.max_carnivores:
                return
            baby_carni = Carnivore(self.params.carnivore_energy_value, self.params, new_genes, self, self.rand_instance, new_generation)
            self.carnivores.append(baby_carni)
            self.carnivore_count += 1
            
    def get_foods(self, Animal):
        if isinstance(Animal, Herbivore):
            return self.plants
        elif isinstance(Animal, Carnivore):
            return self.herbivores
    
    def get_mates(self, Animal):
        if isinstance(Animal, Herbivore):
            return self.herbivores
        elif isinstance(Animal, Carnivore):
            return self.carnivores

    def get_predators(self, Animal):
        if isinstance(Animal, Herbivore):
            return self.carnivores
        return []
    
    def remove_element(self, Element):
        try:
            if isinstance(Element, Plant):
                self.plants.remove(Element)
                self.plant_count -= 1
            elif isinstance(Element, Herbivore):
                self.herbivores.remove(Element)
                self.herbivore_count -= 1
                
                self.best_herbivores.append(Element)
                if len(self.best_herbivores) > self.num_best_herbi:
                    self.best_herbivores.pop(0)


            elif isinstance(Element, Carnivore):
                self.carnivores.remove(Element)
                self.carnivore_count -= 1
                
                self.best_carnivores.append(Element)
                if len(self.best_carnivores) > self.num_best_carni:
                    self.best_carnivores.pop(0)

                
        except:
            print("Element not found")

    def run_simulation(self):
        
        for i in range(self.params.sim_epochs):
            print(f'Running simulation epoch {i+1} of {self.params.sim_epochs}')
            

            
            for j in range(self.params.simulation_duration):
                self.update_plants()
                self.update_herbivores()
                self.update_carnivores()
                self.print_sim_status()
                self.update_sim_status()
                self.vis.draw_state(self.herbivores, self.carnivores, self.plants)
                self.sim_iteration += 1
                time.sleep(self.params.sim_iteration_delay)
                if self.herbivore_count == 0 and self.carnivore_count == 0:
                    break
                
            self.generate_mutated_animals()
            self.plants.clear()
            self.plant_count = 0
            self.generate_initial_plants()
            self.epoch_count += 1
            self.sim_iteration = 0

        self.plot_sim_results()
        plt.show()