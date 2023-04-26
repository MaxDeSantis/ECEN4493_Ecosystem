
import numpy as np
from enum import Enum

# Simulated genes:
# 0: breed_energy_cost
# 1: move_energy_cost
# 2: breed_urge_increase
# 3: breed_urge_threshold
# 4: hunger_urge_threshold
# 5: hunger_urge_increase

class GeneticCode:
    class Gene(Enum):
        breed_energy_cost = 0
        move_energy_cost = 1
        breed_urge_increase = 2
        breed_urge_threshold = 3
        hunger_urge_threshold = 4
        hunger_urge_increase = 5
        hunt_success_chance = 6
        prey_flee_chance = 7
    
    def __init__(self, genes:np.ndarray = None):
        
        if genes is not None:
            self.genes = genes
        else:
            self.genes = np.random.randint(1, 30, len(GeneticCode.Gene))
        
            
    def __getitem__(self, key):
        return self.genes[key]

def crossover(genes1:GeneticCode, genes2:GeneticCode) -> GeneticCode:
    crossover_point = np.random.randint(0, len(GeneticCode.Gene))
    new_genes = np.zeros(len(GeneticCode.Gene))
    
    for i in range(len(GeneticCode.Gene)):
        if i < crossover_point:
            new_genes[i] = genes1[i]
        else:
            new_genes[i] = genes2[i]
            
    return GeneticCode(new_genes)




def mutate(genes:GeneticCode, mutation_rate:float) -> GeneticCode:
    new_genes = np.zeros(len(GeneticCode.Gene))
    
    for i in range(len(GeneticCode.Gene)):
        if np.random.rand() < mutation_rate:
            new_genes[i] = np.random.rand()
        else:
            new_genes[i] = genes[i]
            
    return GeneticCode(new_genes)