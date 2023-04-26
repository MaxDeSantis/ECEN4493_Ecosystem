import Utility
from Utility import Position

from Element import Element

class Plant (Element):
    def __init__(self, position:Position, energy_value):
        super().__init__(position, energy_value)