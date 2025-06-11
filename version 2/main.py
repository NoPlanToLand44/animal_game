import functions_lib
from abc import ABC, abstractmethod
from rich.console import Console 
import random
import time

random.seed(time.time())
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
        # create animals using factory pattern 
        self.carn_list = functions_lib.create_entity(self.carn_count, Carnivore)
        self.herb_list = functions_lib.create_entity(self.herb_count, Herbavore)
        functions_lib.randomize_positions(self.grid_map, self.carn_list, self.herb_list)

    def destroy(self,animal_list,animal_id):
        for i, animal in enumerate(animal_list):
            if animal.unique_id == animal_id:
                return animal_list.pop(i)
        return None
   

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
        self.code = int()
        self.mark_for_deletion = False
        

        # # there will be one instance for every animal 
        pass
    def move(self, grid, world):
        # try the directions a few times: 
        directions = [(-1,0),(0,1),(1,0),(0,-1)]
        max_attempts = 25
        for attempt in range(max_attempts):
            dr, dc = random.choice(directions)
            new_row = self.x+dr
            new_col = self.y + dc
            # we check if we are in the bouynds of the map 
            if (new_row < 0 or new_row >= len(grid) or 
            new_col < 0 or new_col >= len(grid[0])):
                continue
            if grid[new_row][new_col] == 0:
                # clear positions and move
                grid[self.x][self.y] = 0
                # update animal 
                self.x = new_row
                self.y = new_col
                # update world
                grid[new_row][new_col] = self.code
                return 
            elif grid[new_row][new_col] == self.code:
                continue
            else:
                if self.code == 1:
                    if random.random() < 0.6:
                        # we need to get the rabits position id
                        # we ensure we get the same instance of world , because we implemented singleton design 
                        rabbit_id = None 
                        for rabbit in world.herb_list:
                            if rabbit.x == new_row and rabbit.y == new_col:
                                rabbit_id = rabbit.unique_id
                                break
                        if rabbit_id:
                            # if rabbit looses we destroy its reccord 
                            world.destroy(world.herb_list, rabbit_id)
                            # we move wolf to Rabbit position 
                            grid[self.x][self.y] = 0
                            self.x = new_row
                            self.y = new_col
                            
                            grid[new_row][new_col] = self.code
                            # clear wolf's position
                            return
                    else: 
                        # if rabbit wins, we keep the old position of the 2 anuimlas 
                        continue
                elif self.code == 2:
                    # if rabbit tries to encounter wolf, it will try not to  , so try another direction 
                    continue
                    
            

    @abstractmethod
    def consume(self):
        # use the destroy() from World 
        pass
    


class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        # adding a refferance code for represantation 
        self.code = 1
        
    def __str__(self):
        return "Wolf"
    
    def consume (self):
        pass
    


class Herbavore(Animal):
    def __init__(self):
        super().__init__()
         # adding a refferance code for represantation 
        self.code = 2
    def __str__(self):
        return "Rabbit"    
    







world = World()
console.print(world.grid_map)
counter = 1
while len(world.herb_list) > 0 :
    for carn in world.carn_list: 
        carn.move(world.grid_map,world)
        
    for herb in world.herb_list: 
        herb.move(world.grid_map,world)

    console.print(world.grid_map)
   

#will need to randomize,which entity moves first to avoid order bias 

# make sure u put in the main loop and exhaustive list 