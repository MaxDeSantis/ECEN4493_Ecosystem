

class SimulationParameters:
    def __init__(self):
        # Simulation size
        self.x_min = -300
        self.x_max = 300
        self.y_min = -300
        self.y_max = 300
        self.num_plants = 400
        self.num_herbivores = 40
        self.num_carnivores = 30
        
        self.plant_spawn_probability = 0.4
        self.plant_spawn_count_max = 10
        
        # Sim runtime
        self.simulation_duration = 100
        self.sim_iteration_delay = 0.05

        # Plant parameters
        self.plant_energy_value = 55
        self.herbivore_energy_value = 400
        self.carnivore_energy_value = 100
        
        self.carnivore_act_range = 2
        self.herbivore_act_range = 2
        
        self.mutation_percentage = 0.1
        
        self.sim_epochs = 5
        
        self.max_herbivores = 10 * self.num_herbivores
        self.max_carnivores = 10 * self.num_carnivores