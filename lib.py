import numpy as np
from rich.console import Console
from rich.table import Table
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
        while not self.rows or self.cols:
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
        try:
            self.initial_herb_population = int(input("Enter the number of herbevores in the world: "))
            self.initial_carn_population = int(input('Enter the number of carnicovers in the world: '))
            if self.initial_herb_population + self.initial_carn_population > (self.rows * self.cols) : 
                console.print('[red]Dont put more animals than there are squares on the map!!! [/red]')
                self._get_population_metrics()
            else:
                return self.initial_herb_population, self.initial_carn_population
        except ValueError: 
            console.print('[red] Pls input valid numbers! [/red]')
            self._get_population_metrics()


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



class Animal:

    def __init__(self):
        self.name = ""
        self.symbol = ""
        self.xy_position = []
        self.unspawned_population = 0
        self.current_population = 0
    
    def get_location_from_world(self):
        pass

    def move_on_grid(self):
        pass



class Carnavore(Animal):
    def __init__(self):
        self.name = ""
        self.symbol = "🐺"
    

    def hunt(self):
        pass



class Herbavore(Animal):
    
    def __init__(self):
        self.name = ""
        self.symbol = "🐰"
    
    def hunted(self):
        pass





world = World()


