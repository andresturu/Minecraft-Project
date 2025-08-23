import pygame
from sys import exit
from random import randint, choice
from map_generator import generate_biome_map

screen_width, screen_height = 960,640 #make sure tile_size multiplies into these cleanly
seed = randint(0,10000)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minecraft 2D')
clock = pygame.time.Clock()



#plains, desert, water, snow, mountain, forest
class Biomes():
    
    BIOME_TEXTURES = { #these don't match or make sense rn, change later
        0: 'graphics/blocks/coral_block_star.png',   # Deep Water
        1: 'graphics/blocks/sand_ugly.png',   # Shallow Water
        2: 'graphics/blocks/grass_top.png',        #(34, 139, 34),   # Grassland
        3: 'graphics/blocks/oak_log_side.png',     # Forest
        4: 'graphics/blocks/stone_generic.png', # Mountain
        5: 'graphics/blocks/grass_top.png' # Snow
    }
    
    def __init__(self):
        self.tile_size = 8 
        tile_width = int(screen_width /self.tile_size) #for making the biome_map proportionally smaller
        tile_height = int(screen_height /self.tile_size)
        resolution_scale = int(200/self.tile_size)
        self.biome_map = generate_biome_map(tile_width, tile_height, seed, resolution_scale)#returns 2D NumPy array filled with integers 0 to 5 representing biomes
        self.background = pygame.Surface((screen_width, screen_height))
    
        self.render_colors()

    def render_colors(self):
        for y in range (int(screen_height/self.tile_size)):
            for x in range (int(screen_width/self.tile_size)):
                texture_path = Biomes.BIOME_TEXTURES[self.biome_map[y,x]]    
                texture_surf = pygame.image.load(texture_path).convert_alpha()
                scaled_texture_surf = pygame.transform.scale(texture_surf, (self.tile_size, self.tile_size))
                self.background.blit(scaled_texture_surf, (x *self.tile_size, y *self.tile_size))

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
    clock.tick(60)