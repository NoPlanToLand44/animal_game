import numpy as np
from rich.console import Console
from rich.table import Table
import random
console = Console()

class World():

    def __init__(self ):
        self.empty_symbol = "⬜"
        self.rows = 0
        self.cols = 0
        self.initial_herb_population = 0
        self.initial_carn_population = 0
        # we ask the user to define the dimentions of the map 
        self._get_grid_dimentions()
        populated_grid = self._create_game_grid(self.rows, self.cols)
        console.print('This is the initial map: ')
        console.print(populated_grid)
        # we ask for population metrics
        self._get_population_metrics()
        console.print('Randomizing the positions of each animal:  ')
        # creating the Null world with zeroes , so its easier to work with it and after that well convert it to graphics
        self.grid_array = np.ndarray((self.rows * self.cols))
        # setting the conversion map of the array_world to graphics world  
        self.grid_graphics_map = {
        0: "⬜",
        1: "🐺",
        2: "🐰",
        3: "🐺🐰"
        }
        self._initialize_populated_grid()
        
        

    def _get_grid_dimentions(self):
        # we put a 30 squares limit so the world doesnt get too big
        while not ( self.rows and self.cols ):
            try:
                self.rows = int(input("Enter the number of rows of the world: "))
                self.cols = int(input('Enter the number of the cols of the world: '))
                if self.rows > 30 or self.cols > 30  or self.rows < 0 or self.cols < 0: 
                    console.print('Pls dont make the map too big')
                    self.rows = 0 
                    self.cols = 0
                elif self.rows == 0 or self.cols == 0 : 
                    console.print('[red] Dont make it 0!!!! we cant have a map with 0 .... [/red]')
                    continue
                else:
                    return self.rows, self.cols
            except ValueError: 
                console.print('[red] Pls input valid int numbers! between 1 and 30 !!! [/red]')
                
    
    def _get_population_metrics(self):
        
        # making sure we have less animals than there are grids on the map 
        while not (self.initial_carn_population and self.initial_herb_population):
            try:
                self.initial_herb_population = int(input("Enter the number of herbevores in the world: "))
                self.initial_carn_population = int(input('Enter the number of carnicovers in the world: '))
                if self.initial_herb_population + self.initial_carn_population > (self.rows * self.cols) : 
                    console.print('[red]Dont put more animals than there are squares on the map!!! [/red]')
                    self.initial_herb_population = 0
                    self.initial_carn_population = 0 
                elif self.initial_herb_population == 0 or self.initial_carn_population == 0:
                    console.print('[red] Dont make the pop metrics 0 ,daimn it!!! !!!! we cant have a simulation with 0 .... [/red]')
                    continue
                else:
                    return self.initial_herb_population, self.initial_carn_population
            except ValueError: 
                console.print('[red] Pls input valid numbers! [/red]')
                


    def _create_game_grid(self, rows,cols):
        table = Table(show_header=False, show_edge=False, padding = 0)
        for col in range(cols):
            table.add_column(justify="center", width=4)

        for row in range(rows):
            row_data = self.empty_symbol * cols
            table.add_row(*row_data)
        return table
    
    def _map_grid_to_graphics(self, grid_array, the_map:dict ):

        """
        Mapping the graphics to the logic array that we made
        """
        

        graphic_grid = np.vectorize(the_map.get)
        result = graphic_grid(grid_array)
        return console.print(result)

    def _initialize_populated_grid(self):
        values = [1] * self.initial_carn_population + [2] * self.initial_herb_population + [0] * (self.grid_array.size - self.initial_carn_population - self.initial_herb_population)
        np.random.shuffle(values)   
        self.grid_array = np.array(values).reshape((self.rows, self.cols))


        self.graphics = self._map_grid_to_graphics(self.grid_array, self.grid_graphics_map)
        return self.graphics

    def has_herbavores(self):
        pass

    def move_all_animals(self):
        pass

    def resolve_encounters(self): 
        pass

    def display_state(self):
        pass



class Animal:

    def __init__(self):
        self.name = ""
        self.number = int
        self.symbol = ""
        self.xy_position = []

    def get_location(self, grid, number_code):
        # get the coordinates of all carnivores and shuffle their positions to avoid moving bias 
        position = list((zip(*np.where((grid == number_code )))))
        np.random.shuffle(position)
        return position
    


    def move(self, grid, number_code):
        rows, cols = grid.shape
        positions = self.get_location(grid, self.number)
        for r, c in positions:
            # choose a random direction : 
            dr, dc = random.choice([(0,-1), (-1,0), (0,1), (1,0)])
            nr , nc = r + dr , c + dc
            # stay in the map and move only if the dest is empty
            if 0 <= nr < rows and  0 <= nc  < cols and grid[nr, nc] == 0:
                grid[nr, nc] = number_code
                grid[r,c] = 0
        return grid

    def handle_collisions(self):
        pass



class Carnavore(Animal):

    def __init__(self):
        super().__init__()
        self.number = 1
        self.name = 'wolf'
        self.symbol = "🐺"
        self.current_population = 0

    

    def hunt(self):
        pass



class Herbavore(Animal):
    
    def __init__(self):
        super().__init__()
        self.number = 2
        self.name = "rabbit"
        self.symbol = "🐰"
        self.current_population = 0
    
    def hunted(self):
        pass





world = World()
wolf = Carnavore()
console.print(world.grid_array)
console.print(wolf.move(world.grid_array, wolf.number))
