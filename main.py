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
class Biomes(): #making it inherit from sprite class is overkill unless I want to make each specific tile interactable with the player
    
    BIOME_TEXTURES = { #these don't match or make sense rn, change later
        0: ['graphics/water/deep_water_1.png', 'graphics/water/deep_water_2.png'],   # Deep Water, want to alternate between these two
        1: 'graphics/blocks/desert_block.png',   # Desert
        2: 'graphics/blocks/grass_top.png',      # Grassland
        3: 'graphics/blocks/oak_log_side.png',     # Forest
        4: 'graphics/blocks/stone_generic.png', # Mountain
        5: 'graphics/blocks/snow.png' #Snow
    }
    
    def __init__(self):
        self.tile_size = 16 
        tile_width = int(screen_width /self.tile_size) #for making the biome_map proportionally smaller
        tile_height = int(screen_height /self.tile_size)
        resolution_scale = int(200/self.tile_size)
        self.water_index = 0
        self.biome_map = generate_biome_map(tile_width, tile_height, seed, resolution_scale)#returns 2D NumPy array filled with integers 0 to 5 representing biomes
        self.background = pygame.Surface((screen_width, screen_height))

    
        self.render_images()

    def render_water(self, screen):
        for y in range (int(screen_height/self.tile_size)):
            for x in range (int(screen_width/self.tile_size)):
                if self.biome_map[y,x] == 0: 
                    texture_path = Biomes.BIOME_TEXTURES[self.biome_map[y,x]][int(self.water_index)]    
                    texture_surf = pygame.image.load(texture_path).convert_alpha()
                    scaled_texture_surf = pygame.transform.scale(texture_surf, (self.tile_size, self.tile_size))
                    screen.blit(scaled_texture_surf, (x *self.tile_size, y *self.tile_size))


    def render_images(self):
        for y in range (int(screen_height/self.tile_size)):
            for x in range (int(screen_width/self.tile_size)):
                
                if self.biome_map[y,x] == 0: 
                    continue #skips this if statement, the tile is meant to be a water square
                else:
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
    
    # Background
    world.draw_world(screen)
    world.water_index += 0.015 
    if world.water_index > len(Biomes.BIOME_TEXTURES[0]): world.water_index = 0
    world.render_water(screen)
    
    pygame.display.update()
    clock.tick(60)