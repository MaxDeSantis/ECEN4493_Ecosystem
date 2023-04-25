
import random

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def distance_between_positions(pos1, pos2):
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

def random_position(random_instance, x_min, x_max, y_min, y_max):
    x = random_instance.randint(x_min, x_max)
    y = random_instance.randint(y_min, y_max)
    return Position(x, y)
    