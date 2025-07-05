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
    
    def add_entity(self, animal):
        # this is the only place , where we add entites in Cell, so we also update their coordinates. 
        self.populous.append(animal)
        self.update_entities_coordinates()

    def remove_entity(self, animal):
        if len(self.populous) > 0 : 
            self.populous.remove(animal)


    def update_entities_coordinates(self):
        if len(self.populous) > 0:
            for entity in self.populous:
                entity.x = self.x
                entity.y = self.y

    def is_cell_full(self):
        # if we have more than 2 animals in 1 cell we will treat it as full 

        if len(self.populous) >= 2: 
            return True
        return False 

    def resolve_conflicts(self):
        # we want to be sure the cell contains 2 diferent types of animals : 
        if len(self.populous) > 1 :
            # we make sure one of the animals is of type carn
            carn = [o for o in self.populous if isinstance(o,Carnivore)]
            herb = [o for o in self.populous if isinstance(o, Herbavore)]
            if carn and herb: 
                if random.random() < 0.6:
                    carn[0].hunt()
                else: 
                    console.print(f"herb id = {herb[0].unique_id} got lucky ")
            
    
    def choose_entity(self):
        # if the populous list is empty we will return false and not call .move() on it  
        if not self.populous:
            return False
        # filter out dead animals: 
        alive_animals = [animal for animal in self.populous if not getattr(animal, "is_dead" , False)]
        if not alive_animals:
            return False
        # if there is more than 1 animal on any cell , choose a random animal to move from the cell 
        # returns the animal object to be moved
        if len(alive_animals) > 1:
            return random.choice(alive_animals)
        return alive_animals[0]

    

    
class DataConsoleCollection():
    #we make it a singleton because we collect the data only once  
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self,"_initialized"):
            return
        self._initialized = True
        self.grid_rows, self.grid_cols = self._get_user_inputs()
        self.carn_count, self.herb_count = self._get_animal_metrics_from_user(self.grid_rows, self.grid_cols)
    

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


class World:
    # we will use singleton pattern to make sure we create only 1 instance of that class cause we dont need more than 1 world 
    _instance = None
    def __new__ (cls, *args, **kwargs):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, grid_rows = 0, grid_columns = 0, carn_count = 0 , herb_count = 0):
        # checking if the singleton was already instantiated so we dont run the __init__ () again 
        if hasattr(self, "_initialized"):
            return
        self._initialized = True 
        # get grid and animal count inputs from user
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.carn_count = carn_count
        self.herb_count = herb_count
        # initialize the grid map of the world 
        self.grid_map = self._fill_map(self.grid_rows, self.grid_columns)     
        self.grid_map = self._fill_world(self.grid_map, self.carn_count, self.herb_count)
        self.grid_map = self._randomize_positions(self.grid_map)
      
        

    def _fill_map(self, rows, cols):
        # we create the map of Cell()  objects, where each knows its own coordinates 
        grid = self._initialize_map( rows,cols)
        for i in range(rows) : 
            for j in range(cols): 
                grid[i,j] = Cell(i,j)
        return grid 
    
    def _initialize_map(self, rows, columns):
        # initialize the map with empty slots 
        grid_map = np.empty((rows,columns), dtype = object)
        
        return grid_map



    def _randomize_positions(self, grid ):
        np.random.shuffle(grid)
        grid = self._reset_cell_coordinates(grid)
        return grid
        

    def _fill_world(self, grid,  carn_count, herb_count):
        # this function fills the world with animal objects , assigning animals to each cell 
        shape = grid.shape
        flatten_grid = np.ndarray.flatten(grid)
        for i in range(carn_count):
            flatten_grid[i].add_entity(Carnivore())
        for i in range(carn_count, carn_count + herb_count):
            flatten_grid[i].add_entity(Herbavore())
        filled_grid = np.reshape(flatten_grid, shape = shape)
        return filled_grid
    
    def _reset_cell_coordinates(self, grid):
        # meant to only be used within the class, after an initial shuffle
        rows, cols = grid.shape
        for i in range(rows) : 
            for j in range(cols): 
                grid[i,j].x = i 
                grid[i,j].y = j
                grid[i,j].update_entities_coordinates()
        return grid 

    def is_between_bounds(self, x, y):

        # returns True if we are inside the map , False if we are outside
        rows, cols = self.grid_map.shape
        
        # check if we are still inside the map 
        if x >= rows or x < 0 or y >= cols or y < 0 :
            return False
        return True

    def fetch_cell(self, x, y):
        grid = self.grid_map
        cell = grid[x,y]
        return cell
    
    def has_herbavores(self):
        # will return True as long as there is any herbavores in the world : 
        for c in self.grid_map.flat:
            for a in c.populous:
                if a: 
                    if isinstance(a,Herbavore):
                        return True
        return False


      
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
        
    def _choose_random_direction(self):
        # to be used internally  only, potentially expand the possible movements 
        dx, dy = random.choice([(0, -1),(-1, 0),(0, 1),(1, 0),(-1, -1),(-1, 1),(1, 1),(1, -1),])
        return dx, dy
        # # there will be one instance for every animal , which will be contained in Cell ()
    def move(self):
        
        
        # choose a random direction of movement
        dx, dy = self._choose_random_direction()
        
        # compute new coordinates
        new_x = self.x + dx
        new_y = self.y + dy 
        # chekc if we are inside the map and if the cell doesnt have 2 or more animals in it because as of this version, 
        # the resolve() method will resolve only 2 animals 
        if World().is_between_bounds(new_x, new_y) and (not World().fetch_cell(new_x, new_y).is_cell_full()):
            
            # remove animal from world 
            World().grid_map[self.x, self.y].remove_entity(self)
            # tell set animal about the new coordinates
            self.x = new_x
            self.y = new_y
            
            # tell world, where is the new animal 
            World().grid_map[new_x, new_y].add_entity(self)







class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        # define coordinates, where they live 

    def __str__(self):
        return "W"
    

    def hunt(self):
        cell = World().fetch_cell(self.x, self.y)
        # we assume there is only 1 herb that can die 
        herb = [o for o in cell.populous if isinstance(o, Herbavore) and not getattr(o, "is_dead", False)]
        if herb:
            herb[0].die()
            console.print(f"Carn {self.unique_id} killed herb {herb[0].unique_id}")
    


class Herbavore(Animal):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "R"    
    
    def die(self):
        if self.x is not None and self.y is not None:
            try:
                # delete it from world 
                cell = World().fetch_cell(self.x, self.y)
                cell.remove_entity(self)
                # delete its own coordinates
                self.x = None
                self.y = None 
                self.is_dead = True
            except (IndexError, ValueError) as e: 
                console.print(f"Could not remove animal {self.unique_id} from cell : {self.x} , {self.y}")
            



data = DataConsoleCollection()

world = World(grid_rows = data.grid_rows , grid_columns = data.grid_cols, carn_count = data.carn_count, herb_count = data.herb_count)
# checking if world randopmizes the map and checking for some random ids and tags 
console.print(world.grid_map)
# using arr.flat() cause it returns an iterator over my entire world arrray without changing it inplace 
# we move all the elements in the map, according to our rules 
while World().has_herbavores():
    moved_animals = set()

    for c in World().grid_map.flat:
        animal = c.choose_entity()
        if animal and animal.unique_id not in moved_animals:
            animal.move()
            moved_animals.add(animal.unique_id)
            #console.print(world.grid_map)
             
    console.print() 
    console.print(f"Before resolution:")
    console.print(world.grid_map)
    console.print() 
    for c in World().grid_map.flat:
        c.resolve_conflicts()
    
    console.print(f"After resolution:")
    console.print(world.grid_map)
    console.print() 
    console.print("-" * 50)  
    console.print()  