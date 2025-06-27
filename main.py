from rich.console import Console 
import numpy as np
import random 
import time

random.seed(time.time())
console = Console()

class Cell:
    # we want to generate all cells at the creation of the world and the world will know about the cells and each cell will know about 
    # whats on it 
    _id_counter = 0

    def __init__(self,x,y):
        type(self)._id_counter +=1
        self.unique_id = type(self)._id_counter
        # define cell coordinates 
        self.x = x
        self.y = y
        # define what lives on that cell: will be a list of objects, epty list is noting and all else will have something in that list  
        self.populous = []

    def __repr__ (self):
        if self.populous:
            # stupid preview for dev purpose, remove after we finish logic 
            return ", ".join(f"{item}{item.unique_id}" for item in self.populous)
        return "N"


class World:
    # we will use singleton pattern to make sure we create only 1 instance of that class cause we dont need more than 1 world 
    _instance = None
    def __new__ (cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # checking if the singleton was already instantiated so we dont run the __init__ () again 
        if hasattr(self, "_initialized"):
            return
        self._initialized = True 
        # get grid and animal count inputs from user
        self.grid_rows, self.grid_columns = self._get_user_inputs()
        self.carn_count, self.herb_count = self._get_animal_metrics_from_user(self.grid_rows, self.grid_columns)
        # initialize the grid map of the world 
        self.grid_map = self._fill_map(self.grid_rows, self.grid_columns)     
        self.grid_map = self._fill_world(self.grid_map, self.carn_count, self.herb_count)
        self.grid_map = self._randomize_positions(self.grid_map)
        self.grid_map = self._feed_coordinates_info_to_animals(self.grid_map)
      
        

    def _fill_map(self, rows, cols, cells_class = Cell ):
        # we create the map of Cell()  objects, where each knows its own coordinates 
        grid = self._initialize_map( rows,cols)
        for i in range(rows) : 
            for j in range(cols): 
                grid[i,j] = cells_class(i,j)
        return grid 
    
    def _initialize_map(self, rows, columns):
        # initialize the map with empty slots 
        grid_map = np.empty((rows,columns), dtype = object)
        
        return grid_map


    def _get_user_inputs(self):
        while True:
            try: 
                rows = int(input("Enter the number of rows: "))
                cols = int(input("enter the  number of cols: "))
                if 1<= rows <=30 and 1<= cols <=30 : 
                    return rows, cols
                else: 

                    console.print("enter valid number!!")
            except ValueError:
                console.print("'[red] Pls input valid int numbers! between 1 and 30 !!! [/red]'")
    

    def _get_animal_metrics_from_user(self, rows , cols):
        # checking if the animals are too many before accepting the count 
        carn = 0
        herb = 0
        while not (carn and herb):
            try: 
                carn = int(input("Enter the number of carns: "))
                herb = int(input("enter the  number of herbs: "))
                if ( carn + herb >= rows * cols) or  (carn <= 0 or herb <=  0): 
                    console.print('dont put thhat many or a few animals in....')
                    carn = 0
                    herb = 0
            except ValueError:
                console.print('[red] Pls input valid int numbers! [/red]')
        return carn, herb
    
    def _randomize_positions(self, grid ):
        np.random.shuffle(grid)
        grid = self._reset_cell_coordinates(grid)
        return grid
        

    def _fill_world(self, grid,  carn_count, herb_count):
        # this function fills the world with animal objects , assigning animals to each cell 
        shape = grid.shape
        flatten_grid = np.ndarray.flatten(grid)
        for i in range(carn_count):
            flatten_grid[i].populous.append(Carnivore())
        for i in range(carn_count, carn_count + herb_count):
            flatten_grid[i].populous.append(Herbavore())
        filled_grid = np.reshape(flatten_grid, shape = shape)
        return filled_grid
    
    def _reset_cell_coordinates(self, grid):
        # meant to only be used within the class, after an initial shuffle
        rows, cols = grid.shape
        for i in range(rows) : 
            for j in range(cols): 
                grid[i,j].x = i 
                grid[i,j].y = j
        return grid 

    def _feed_coordinates_info_to_animals(self, grid):
        # let the animal object know its own coordinates
        rows, cols = grid.shape
        for i in range(rows) : 
            for j in range(cols): 
                if len(grid[i,j].populous) > 0:
                    animal = grid[i,j].populous[0]
                    animal.x = i 
                    animal.y = j
                    # telling animal about the world after all the animals are  assigned a spot 
                    animal.world = self
        return grid


      
class Animal:
      # making a unique ID for each instance of this class if needed down the road 
    _id_counter = 0
    # containing all the general animal logic 
    def __init__(self):
        type(self)._id_counter +=1 
        self.unique_id = type(self)._id_counter
        # each animal needs to know , where they are on the grid 
        self.x = 0
        self.y = 0
        # we need this to ensure we are not calling move before the world is initiated 
        self.world = None

        # # there will be one instance for every animal , which will be contained in Cell ()
    def move(self):
        # we check for world initialization 
        if not self.world:
            console.print(f"Animal {self.unique_id} has no reff")
            return
        
        # choose a random direction of movement
        dx, dy = self._choose_random_direction()
        # chekc if we are inside the map : 
        if self._check_direction_validity(dx, dy):
            # compute new coordinates
            new_x = self.x + dx
            new_y = self.y + dy
            # remove animal from world 
            self.world.grid_map[self.x,self.y].populous.remove(self)
            # tell set animal about the new coordinates
            self.x = new_x
            self.y = new_y
            
            # tell world, where is the new animal 
            self.world.grid_map[new_x, new_y].populous.append(self)



    
    def _choose_random_direction(self):
        # to be used internally  only, potentially expand the possible movements 
        dx, dy = random.choice([(0,-1),(-1,0),(0,1),(1,0)])
        return dx, dy

    def _check_direction_validity(self, dx, dy):
        # we check if world is fully initialized before we do operations with it 
        if not self.world:
            return False
        # returns True if we are inside the map , False if we are outside
        rows, cols = self.world.grid_map.shape
        new_row = self.x + dx
        new_col = self.y + dy
        # check if we are still inside the map 
        if new_row >= rows or new_row < 0 or new_col >= cols or new_col < 0 :
            return False
        return True


class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        # define coordinates, where they live 

    def __str__(self):
        return "W"
    

    def eat(self):
        # wrtie here attack logic 
        pass
    


class Herbavore(Animal):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "R"    
    
    def die(self):
        # write here the dying logic 
        pass





world = World()
# checking if world randopmizes the map and checking for some random ids and tags 
console.print(world.grid_map)
world.grid_map[1,1].populous[0].move()
console.print(world.grid_map)
