
import random
import math

import SimulationParameters

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_string(self):
        return f'Position({self.x}, {self.y})'

    def __str__(self) -> str:
        return self.get_string()
    
    def __repr__(self) -> str:
        return self.get_string()
        
def distance_between_positions(pos1, pos2):
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

def direction_between_positions(pos1, pos2):
    if pos1.x == pos2.x:
        if pos2.y > pos1.y:
            return math.pi / 2
        else:
            return 3 * math.pi / 2
    
    return math.atan2(pos2.y - pos1.y, pos2.x - pos1.x)

def opposite_direction(direction):
    return (direction + math.pi) % (2 * math.pi)

def random_position(random_instance, params):
    x = random_instance.randint(params.x_min, params.x_max)
    y = random_instance.randint(params.y_min, params.y_max)
    return Position(x, y)
    
def random_direction(random_instance):
    phi = random_instance.uniform(0, 2 * math.pi)
    return phi

def move_to(position, direction, distance, params:SimulationParameters):
    x = position.x + distance * math.cos(direction)
    y = position.y + distance * math.sin(direction)
    
    new_pos = update_bounds(Position(x, y), params)
    return new_pos

def update_bounds(position:Position, params:SimulationParameters):
    if position.x < params.x_min:
        position.x = params.x_min
    if position.x > params.x_max:
        position.x = params.x_max
    if position.y < params.y_min:
        position.y = params.y_min
    if position.y > params.y_max:
        position.y = params.y_max
        
    return position