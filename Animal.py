
from GeneticCode import GeneticCode

from SimulationParameters import SimulationParameters


import random
import Utility

from enum import Enum

from Element import Element

import Plant
import math

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
        self.hunts = 0
        self.target_food = None
        self.breed_target = None
        
        self.baby_daddy = None
        self.pregnant = False
        self.gestation_iterations = 0
        
        # State variables
        self.hunger = 0
        self.breed_urge = 0
        self.energy = 200
        self.direction = Utility.random_direction(self.rand_instance)
        
        self.parent1 = None
        self.parent2 = None
    
    # ACTION DEFINITIONS ------------------------------------------------------------------------- 
    
    def ACTION_die(self):
        self.manager.remove_element(self)
        
    def ACTION_give_birth(self):
        num_babies = math.ceil(self.genes[GeneticCode.Gene.litter_size.value])
        
        for i in range(num_babies):
            self.manager.spawn_animal(self, self.baby_daddy)
            
        self.pregnant = False
        self.gestation_iterations = 0
        self.baby_daddy = None
    
    def BEHAVIOR_attempt_eat(self, foods):
        #print("Attempting to eat")
        #print('Target: ', self.target_food)
        if self.target_food is None or self.hunts > self.genes[GeneticCode.Gene.hunt_tenacity.value]:
            self.target_food = self.FIND_nearest_food(foods)
            self.hunts = 0
        
        # Wander
        if self.target_food is None:
            self.BEHAVIOR_wander()
            return
        #print('New target: ', self.target_food)
        #print('Found food')
        self.hunts += 1
        result = self.ACTION_move_and_act(self.target_food.position)
        #print(f'Eating {self.target_food}, result: {result}')
        if result:
            # Carnivores may fail to catch their prey
            if isinstance(self.target_food, Plant.Plant):
                self.ACTION_eat(self.target_food)
                #self.hunger -= nearest_food.energy_value
                self.hunger = 0
                self.speed = 4
                self.target_food = None
                
            elif self.rand_instance.randint(1, 30) < self.genes[GeneticCode.Gene.hunt_success_chance.value]:
                self.ACTION_eat(self.target_food)
                self.hunger = 0
                self.target_food = None
            else:
                self.target_food.speed = 7
        
    def ACTION_eat(self, food):
        self.energy += food.energy_value
        self.manager.remove_element(food)
    
    def BEHAVIOR_attempt_breed(self, mates):

        if self.breed_target is None:
            self.breed_target = self.FIND_nearest_mate(mates)
            if self.breed_target is None:
                self.BEHAVIOR_wander()
                return
        self.breed_target.bread_target = self
        result = self.ACTION_move_and_act(self.breed_target.position)
        #print(f'Breeding with {self.breed_target}, result: {result}')
        if result:
            self.ACTION_breed(self.breed_target)

    def ACTION_breed(self, other):
        if self is other:
            return
        
        self.breed_urge = 0
        other.breed_urge = 0
        self.energy -= self.genes[GeneticCode.Gene.breed_energy_cost.value]
        other.energy -= other.genes[GeneticCode.Gene.breed_energy_cost.value]
        self.breed_target = None
        other.breed_target = None
        self.pregnant = True
        self.baby_daddy = other
        #print(f'Animal {self} is pregnant with {other}')
        
    def BEHAVIOR_attempt_flee(self, predator):
        chance = self.rand_instance.randint(1, 30)
        if chance < self.genes[GeneticCode.Gene.prey_flee_chance.value]:
            self.ACTION_flee()
    
    def ACTION_flee(self):
        dir_predator = Utility.direction_between_positions(self.position, self.nearest_predator.position)
        dir = Utility.opposite_direction(dir_predator)
        
        self.ACTION_move(dir)
                
    def BEHAVIOR_wander(self):
        if self.rand_instance.randint(1, 30) < self.genes[GeneticCode.Gene.wander_dir_change_chance.value]:
            self.direction = Utility.dir_lerp(Utility.random_direction(self.rand_instance), self.direction, self.genes[GeneticCode.Gene.wander_dir_change.value])
            
        self.ACTION_move(self.direction)
    
    def ACTION_move(self, direction):
        new_pos  = Utility.move_to(self.position, direction, self.speed, self.params)
        dist = Utility.distance_between_positions(self.position, new_pos)
        #print(f'Moving {dist} units')
        self.position = new_pos
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
           # print('Fleeing')
            return self.Behaviors.ATTEMPT_FLEE
        elif self.hunger > self.genes[GeneticCode.Gene.hunger_urge_threshold.value]:
            #print('Eating')
            return self.Behaviors.ATTEMPT_EAT
        elif (self.breed_urge > self.genes[GeneticCode.Gene.breed_urge_threshold.value]) and not self.pregnant:
            #print('Breeding')
            return self.Behaviors.ATTEMPT_BREED
        else:
            #print('Wandering')
            return self.Behaviors.ATTEMPT_WANDER
    
    def UPDATE_state(self):
        self.hunger += self.genes[GeneticCode.Gene.hunger_urge_increase.value]
        self.breed_urge += self.genes[GeneticCode.Gene.breed_urge_increase.value]
        self.energy -= 5 # lose 5 energy per turn
    
    # SIM INTERACTION ------------------------------------------------------------------------- 

    def SET_parents(self, p1, p2):
        self.parent1 = p1
        self.parent2 = p2
        
    def FIND_nearest_mate(self, mates):
        nearest_mate = None
        nearest_distance = float('inf')
        for mate in mates:
            if not self.IS_mate_valid(mate):
                continue
            
            distance = Utility.distance_between_positions(self.position, mate.position)
            if distance < nearest_distance:
                nearest_mate = mate
                nearest_distance = distance
        #print(f'Nearest mate: {nearest_mate}')
        return nearest_mate

    # Don't breed with self, don't breed with parents, don't breed with siblings and don't breed unconsentually
    def IS_mate_valid(self, mate) ->bool:
        if mate is self or mate.pregnant:
            return False
        
        if mate == self.parent1 or mate == self.parent2:
            return False
        
        if self == mate.parent1 or self == mate.parent2:
            return False
        
        if mate.breed_urge < mate.genes[GeneticCode.Gene.breed_urge_threshold.value]:
            return False
        
        if mate.hunger > mate.genes[GeneticCode.Gene.hunger_urge_threshold.value]:
            return False
        
        if self.parent1 is not None and self.parent2 is not None:
            if self.parent1 == mate.parent1 or self.parent1 == mate.parent2:
                return False
            
            if self.parent2 == mate.parent1 or self.parent2 == mate.parent2:
                return False
        
        return True

    
    def FIND_nearest_food(self, foods):
        valid_foods = []
        for food in foods:
            distance = Utility.distance_between_positions(self.position, food.position)
            if distance < self.genes[GeneticCode.Gene.hunt_selection_range.value]:
                valid_foods.append(food)

        if len(valid_foods) == 0:
            return None
        else:
            return self.rand_instance.choice(valid_foods)

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
            
        if self.pregnant:
            self.gestation_iterations += 1
        
        if self.gestation_iterations >= self.genes[GeneticCode.Gene.gestation_period.value]:
            self.ACTION_give_birth()
            
        if self.energy < 0:
            self.ACTION_die()
        else:
            self.UPDATE_state()