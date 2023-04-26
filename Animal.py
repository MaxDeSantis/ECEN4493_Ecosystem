
from GeneticCode import GeneticCode

from SimulationParameters import SimulationParameters


import random
import Utility

from enum import Enum

from Element import Element

import Plant


class Animal (Element):
    
    class Behaviors(Enum):
        ATTEMPT_EAT = 0
        ATTEMPT_BREED = 1
        ATTEMPT_WANDER = 2
        ATTEMPT_FLEE = 3
    
    def __init__(self, energy_value, sim_params:SimulationParameters, genetic_code:GeneticCode, manager, random_instance, generation=0):
        super().__init__(Utility.random_position(random_instance, sim_params), energy_value)
        
        self.params = sim_params
        self.manager = manager
        self.generation = generation
        self.rand_instance = random_instance
        
        # Attributes
        self.speed = 3
        self.genes = genetic_code
        self.eat_distance = 0
        
        # State variables
        self.hunger = 0
        self.breed_urge = 0
        self.energy = 200
        self.direction = Utility.random_direction(self.rand_instance)
    
    # ACTION DEFINITIONS ------------------------------------------------------------------------- 
    
    def ACTION_die(self):
        self.manager.remove_element(self)
    
    def BEHAVIOR_attempt_eat(self, foods):
        #print("Attempting to eat")
        nearest_food = self.FIND_nearest_food(foods)
        if nearest_food is None:
            return
        
        result = self.ACTION_move_and_act(nearest_food.position)
        if result:
            # Carnivores may fail to catch their prey
            if isinstance(nearest_food, Plant.Plant):
                self.ACTION_eat(nearest_food)
                #self.hunger -= nearest_food.energy_value
                self.hunger = 0
                self.speed = 4
                
            elif self.rand_instance.randint(1, 30) < self.genes[GeneticCode.Gene.hunt_success_chance.value]:
                self.ACTION_eat(nearest_food)
                #self.hunger -= nearest_food.energy_value
                self.hunger = 0
            else:
                nearest_food.speed = 7
        
    def ACTION_eat(self, food):
        self.energy += food.energy_value
        self.manager.remove_element(food)
    
    def BEHAVIOR_attempt_breed(self, mates):
        nearest_mate = self.FIND_nearest_mate(mates)
        if nearest_mate is None:
            return
        
        result = self.ACTION_move_and_act(nearest_mate.position)
        
        if result:
            self.ACTION_breed(nearest_mate)

    def ACTION_breed(self, other):
        if self is other:
            return
        
        self.breed_urge = 0
        other.breed_urge = 0
        self.energy -= self.genes[GeneticCode.Gene.breed_energy_cost.value]
        other.energy -= other.genes[GeneticCode.Gene.breed_energy_cost.value]
        
        self.manager.breed_animals(self, other)
        
    def BEHAVIOR_attempt_flee(self, predator):
        chance = self.rand_instance.randint(1, 30)
        if chance < self.genes[GeneticCode.Gene.prey_flee_chance.value]:
            self.ACTION_flee()
    
    def ACTION_flee(self):
        dir_predator = Utility.direction_between_positions(self.position, self.nearest_predator.position)
        dir = Utility.opposite_direction(dir_predator)
        
        self.ACTION_move(dir)
                
    def BEHAVIOR_wander(self):
        self.direction = Utility.random_direction(self.rand_instance)
        self.ACTION_move(self.direction)
    
    def ACTION_move(self, direction):
        self.position = Utility.move_to(self.position, direction, self.speed, self.params)
        self.energy -= self.genes[GeneticCode.Gene.move_energy_cost.value]
    
    # Return true if the animal has reached the destination, otherwise move and return false
    def ACTION_move_and_act(self, position):
        dist = Utility.distance_between_positions(self.position, position)
        
        if dist < self.act_range:
            self.position = position
            return True
        else:
            self.direction = Utility.direction_between_positions(self.position, position)
            self.ACTION_move(self.direction)
            return False
            
        
    def ACTION_select_behavior(self):
        
        self.nearest_predator = self.FIND_nearest_predator(self.manager.get_predators(self))
        if self.nearest_predator is not None and Utility.distance_between_positions(self.position, self.nearest_predator.position) < self.flee_range:
            return self.Behaviors.ATTEMPT_FLEE
        elif self.hunger > self.genes[GeneticCode.Gene.hunger_urge_threshold.value]:
            return self.Behaviors.ATTEMPT_EAT
        elif self.breed_urge > self.genes[GeneticCode.Gene.breed_urge_threshold.value]:
            return self.Behaviors.ATTEMPT_BREED
        else:
            return self.Behaviors.ATTEMPT_WANDER
    
    def UPDATE_state(self):
        self.hunger += self.genes[GeneticCode.Gene.hunger_urge_increase.value]
        self.breed_urge += self.genes[GeneticCode.Gene.breed_urge_increase.value]
        self.energy -= 1 # lose 5 energy per turn
    
    # SIM INTERACTION ------------------------------------------------------------------------- 

    def FIND_nearest_mate(self, mates):
        nearest_mate = None
        nearest_distance = float('inf')
        for mate in mates:
            if mate is self:
                continue
            distance = Utility.distance_between_positions(self.position, mate.position)
            if distance < nearest_distance:
                nearest_mate = mate
                nearest_distance = distance
        return nearest_mate
    
    def FIND_nearest_food(self, foods):
        nearest_food = None
        nearest_distance = float('inf')
        for food in foods:
            distance = Utility.distance_between_positions(self.position, food.position)
            if distance < nearest_distance:
                nearest_food = food
                nearest_distance = distance
        return nearest_food

    def FIND_nearest_predator(self, predators):
        nearest_predator = None
        nearest_distance = float('inf')
        if len(predators) == 0:
            return None
        
        for p in predators:
            distance = Utility.distance_between_positions(self.position, p.position)
            if distance < nearest_distance:
                nearest_predator = p
                nearest_distance = distance
        return nearest_predator
    
    def SIM_update(self):
        
        next_behavior = self.ACTION_select_behavior()
        
        if next_behavior == self.Behaviors.ATTEMPT_EAT:
            self.BEHAVIOR_attempt_eat(self.manager.get_foods(self))
        elif next_behavior == self.Behaviors.ATTEMPT_BREED:
            self.BEHAVIOR_attempt_breed(self.manager.get_mates(self))
        elif next_behavior == self.Behaviors.ATTEMPT_FLEE:
            self.BEHAVIOR_attempt_flee(self.nearest_predator)
        else:
            self.BEHAVIOR_wander()
            
        if self.energy < 0:
            self.ACTION_die()
        else:
            self.UPDATE_state()