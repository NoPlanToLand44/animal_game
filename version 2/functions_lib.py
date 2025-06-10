from abc import ABC, abstractmethod
import numpy as np
from rich.console import Console
console = Console()

def get_user_inputs():
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
def initialize_map(rows, columns):
    # initialize the map with empty slots 
    grid_map = np.zeros((rows,columns))
    return grid_map

def get_animal_metrics_from_user(rows , cols):
    # checking if the animals are too many before accepting the count 
    carn = 0
    herb = 0
    while not (carn and herb):
        try: 
            carn = int(input("Enter the number of carns: "))
            herb = int(input("enter the  number of herbs: "))
            if carn + herb >= rows * cols : 
                console.print('dont put thhat many animals in....')
                carn = 0
                herb = 0
        except ValueError:
            console.print('[red] Pls input valid int numbers! [/red]')
    return carn, herb

def create_entity(entity_count:int,animal_class):
    entity_list = []
    # create anything on the grid 
    for i in range(entity_count):
        entity_list.append(animal_class())
    return entity_list


def randomize_positions(grid, *animals_lists):
    for animal_list in animals_lists:
        for animal in animal_list:
            empty_positions = np.argwhere(grid == 0)
            if len(empty_positions) == 0:
                raise ValueError('No empty positions avalable for animal placement')
            
            random_index = np.random.randint(0, len(empty_positions))
            selected_position = empty_positions[random_index]
            animal.x = selected_position[0]
            animal.y = selected_position[1]
            grid[animal.x][animal.y] = animal.code
    return animals_lists
