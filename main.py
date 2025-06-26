from rich.console import Console 
import numpy as np

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

        return (f"Cell {self.x}, {self.y}")


class World:
    # we will use singleton pattern to make sure we create only 1 instance of that class cause we dont need more than 1 world 
    _instance = None
    def __new__ (cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # get grid and animal count inputs from user
        self.grid_rows, self.grid_columns = self._get_user_inputs()
        self.carn_count, self.herb_count = self._get_animal_metrics_from_user(self.grid_rows, self.grid_columns)
        # initialize the grid map of the world 
        self.grid_map = self._fill_map(self.grid_rows, self.grid_columns)     
        self.grid_map = self._fill_world(self.grid_map, self.carn_count, self.herb_count)
        self.grid_map = self._randomize_positions(self.grid_map)

      
        

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
        rows = 0
        cols = 0
        while not (rows and cols):
            try: 
                rows = int(input("Enter the number of rows: "))
                cols = int(input("enter the  number of cols: "))
                if rows > 30 or cols > 30 or rows <= 0 or cols <= 0 : 
                    console.print('Pls dont make the map too big or below zero!')
                    rows = 0
                    cols = 0
            except ValueError:
                console.print('[red] Pls input valid int numbers! between 1 and 30 !!! [/red]')
        return rows, cols 
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
        return grid
        

    def _fill_world(self, grid,  carn_count, herb_count):
        # this function fills the world with animal objects , assigning animals to each cell 
        shape = grid.shape
        flatten_grid = np.ndarray.flatten(grid)
        for i in range(carn_count):
            flatten_grid[i].populous = Carnivore()
        for i in range(carn_count, carn_count + herb_count):
            flatten_grid[i].populous = Herbavore()
        filled_grid = np.reshape(flatten_grid, shape = shape)
        return filled_grid

      
class Animal:
      # making a unique ID for each instance of this class if needed down the road 
    _id_counter = 0
    # containing all the general animal logic 
    def __init__(self):
        type(self)._id_counter +=1 
        self.unique_id = type(self)._id_counter
        
        # # there will be one instance for every animal 
        pass
    def move(self):
        raise NotImplementedError("subclass has to implement this ")

    


class Carnivore(Animal):
    def __init__(self):
        super().__init__()
        # define coordinates, where they live 

    def __str__(self):
        return "Wolf"
    
    def move(self):
        # here we extend the move logic to wolves 
        pass

    def eat(self):
        # wrtie here attack logic 
        pass
    


class Herbavore(Animal):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Rabbit"    
    
    def die(self):
        # write here the dying logic 
        pass

    def move(self):
        # here we extend the move logic to rabbits
        #  
        pass
    




world = World()
# checking if world randopmizes the map and checking for some random ids and tags 
console.print(world.grid_map)
console.print(world.grid_map[1,1].unique_id)
console.print(world.grid_map[1,1].populous)