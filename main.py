import pygame
from sys import exit
from random import randint, choice
from map_generator import generate_biome_map

screen_width, screen_height = 960,640
seed = randint(0,10000)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minecraft 2D')



#plains, desert, water, snow, mountain, forest
class Biomes():
    
    BIOME_COLORS = {
        0: (0, 105, 148),   # Deep Water
        1: (0, 150, 200),   # Shallow Water
        2: (34, 139, 34),   # Grassland
        3: (0, 100, 0),     # Forest
        4: (139, 137, 137), # Mountain
        5: (255, 255, 255), # Snow
    }
    
    def __init__(self):
        self.biome_map = generate_biome_map(screen_width, screen_height, seed)#returns 2D NumPy array filled with integers 0 to 5 representing biomes
        self.background = pygame.Surface((screen_width, screen_height))
        #self.tile_size = 

        self.render_colors()

    def render_colors(self):
        for y in range (screen_height):
            for x in range (screen_width):
                color = Biomes.BIOME_COLORS[self.biome_map[y, x]]
                #surf = pygame.Surf((1,1))
                #surf.fill(color)
                #self.background.blit(surf, (x,y))
                self.background.set_at((x,y), color)

    def draw_world(self, screen):
        screen.blit(self.background, (0,0))

world = Biomes()


while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            pygame.quit() 
            exit() 
    
    world.draw_world(screen)

    
    pygame.display.update()