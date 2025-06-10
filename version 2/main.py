import functions_lib
from abc import ABC, abstractmethod
from rich.console import Console 

console = Console()

class World:
    # we will use singleton pattern to make sure we create only 1 instance of that class cause we dont need more than 1 world 
    _instance = None
    def __new__ (cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # get grid and animal count inputs from user
        self.grid_rows, self.grid_columns = functions_lib.get_user_inputs()
        self.grid_map = functions_lib.initialize_map(self.grid_rows, self.grid_columns)
        self.carn_count, self.herb_count = functions_lib.get_animal_metrics_from_user(self.grid_rows, self.grid_columns)
        # create animals
        self.carn_list = functions_lib.create_entity(self.carn_count, Carnivore)
        self.herb_list = functions_lib.create_entity(self.herb_count, Herbavore)
        functions_lib.randomize_positions(self.grid_map, self.carn_list, self.herb_list)

class Animal:
      # making a unique ID for each instance of this class if needed down the road 
    _id_counter = 0
    # containing all the general animal logic 
    def __init__(self):
        type(self)._id_counter +=1
        self.unique_id = type(self)._id_counter
        # define coordinates, where they live 
        self.x = 0
        self.y = 0
        # # there will be one instance for every animal 
        pass
    def move(self):
        pass

    
    @abstractmethod
    def consume(self):
        pass
    


class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        self.code = 1
        
    def __str__(self):
        return "Wolf"
    


class Herbavore(Animal):
    def __init__(self):
        super().__init__()
        self.code = 2
    def __str__(self):
        return "Rabbit"    
    



world = World()
console.print(world.grid_map)
# show uniquue ID 
console.print(world.carn_list[4].unique_id)
# show coordinates 
console.print(world.carn_list[4].x, world.carn_list[4].y)