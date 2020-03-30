import pygame
from pygame.locals import *
import random

def generate_cells():
    '''
    Generates a random screen of cells. Either black (dead) or red (alive)
    '''
    cells = []
    for y in range(screen_size[1]):
        cells.append([])
        for x in range(screen_size[0]):         
            cells[y].append(random.randint(0,1))

    return cells

def generate_cell_changes(cells):
    '''
    For each cell on screen (both dead and alive), checks for the value of their neighbour (their relative coordinates are saved as constant tuples in cell_checks).
    The sum of neighbour values is then compared and if a change is necessary (cell changes status), the new value and x and y-coordinates of cell are stored in cell_changes which are then returned.
    '''
    cell_checks = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    cell_changes = []

    for y in range(len(cells)):
        for x in range(len(cells[y])):
            adjacent = 0
            for check in cell_checks:
                try:
                    if cells[y + check[1]][x + check[0]] == 1:
                        adjacent += 1
                except:
                    pass
            
            if cells[y][x] == 1:
                if adjacent <= 1 or adjacent >= 4:
                    cell_changes.append([y, x, 0])
            else:
                if adjacent == 3:
                    cell_changes.append([y, x, 1])
    
    return cell_changes

#Defining the size for the grid and the lenght of each quadratic cell.
grid_size = (120, 120)
cell_size = 5            

#initializing pygame
pygame.init()
screen_size = (grid_size[0]*cell_size, grid_size[1]*cell_size)
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game of Life")


#Generating a random cell table
cells = [[random.randint(0, 1) for x in range(grid_size[0])] for y in range(grid_size[1])]

#Preparing the window by drawing each cell to the screen. Black cells are also drawn
for y in range(len(cells)):
    for x in range(len(cells)):
        window.fill((255*cells[y][x], 0, 0), ((y, x), (cell_size, cell_size)))

#Makes sure that the loop is running and reacting to events, but the calculations are paused until updating is true.
running = True
updating = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN: #If a key is pressed, the calculations start
            updating = True
    
    if not updating:
        continue
    
    #Do cell calculations
    cell_changes = generate_cell_changes(cells)
    #Apply cell changes
    for change in cell_changes:
        cells[change[0]][change[1]] = change[2]
        window.fill((255*change[2], 0, 0), ((change[1]*cell_size, change[0]*cell_size), (cell_size, cell_size)))

    #Display cell changes
    pygame.display.update()
    clock.tick(60)