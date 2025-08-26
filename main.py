import pygame
from sys import exit
from random import randint, choice
from map_generator import generate_biome_map
from utils import load_and_prep_player_image


screen_width, screen_height = 1920 , 1280  #make sure tile_size multiplies into these cleanly
biome_map_scalar =8 #biome_map will be x times as large as regular map, to allow scrolling background
seed = randint(0,10000)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minecraft 2D')
clock = pygame.time.Clock()

# Things to do?
# Add like a boundary to the edges to show that the player can't physically go further
# Fix weird blurry right and bottom edge (probably due to offsetting?)
# Add plants to biomes
# Add mobs (friendly and hostile)
# Add health bar
# add enemy damage to health, and combat
# Add sound fx and music


#plains, desert, water, snow, mountain, forest
class Biomes(): #making it inherit from sprite class is overkill unless I want to make each specific tile interactable with the player
    
    tile_size = 32
    tile_width = screen_width //tile_size #width of the visible screen, in tiles
    tile_height = screen_height //tile_size


    BIOME_TEXTURES = { #these don't match or make sense rn, change later
        0: [pygame.transform.scale(pygame.image.load('graphics/water/deep_water_1.png').convert_alpha(), (tile_size, tile_size)), pygame.transform.scale(pygame.image.load('graphics/water/deep_water_2.png').convert_alpha(), (tile_size, tile_size)) ],   # Deep Water, want to alternate between these two
        1: pygame.transform.scale(pygame.image.load('graphics/blocks/desert_block.png').convert_alpha(), (tile_size, tile_size)),   # Desert
        2: pygame.transform.scale(pygame.image.load('graphics/blocks/grass_top.png').convert_alpha(), (tile_size, tile_size)),      # Grassland
        3: pygame.transform.scale(pygame.image.load('graphics/blocks/oak_log_side.png').convert_alpha(), (tile_size, tile_size)),     # Forest
        4: pygame.transform.scale(pygame.image.load('graphics/blocks/stone_generic.png').convert_alpha(), (tile_size, tile_size)), # Mountain
        5: pygame.transform.scale(pygame.image.load('graphics/blocks/snow.png').convert_alpha(), (tile_size, tile_size)) #Snow
    }
    
    def __init__(self):
        resolution_scale = 3200//Biomes.tile_size #make this larger to see smoother/larger biome regions
        self.water_index = 0
        
        self.biome_map = generate_biome_map(biome_map_scalar * Biomes.tile_width,biome_map_scalar * Biomes.tile_height, seed, resolution_scale)#returns 2D NumPy array filled with integers 0 to 5 representing biomes
        print(self.biome_map.shape)
        self.background = pygame.Surface((screen_width, screen_height))

        #scroll_x should always be on left edge of vsisible game screen, scroll_y on the top edge of visible game screen
        self.scroll_x = int(0.5 *(biome_map_scalar * screen_width - screen_width) / Biomes.tile_size) #calculates scroll_x 
        self.scroll_y = int(0.5 *(biome_map_scalar * screen_height - screen_height) / Biomes.tile_size) #calculates scroll_y

        self.scroll_x_max = biome_map_scalar * Biomes.tile_width - Biomes.tile_width #max of how far the player can explore
        self.scroll_y_max = biome_map_scalar * Biomes.tile_height - Biomes.tile_height
        
        self.scroll_x_float = float(self.scroll_x)
        self.scroll_y_float = float(self.scroll_y)
        self.tile_offset_x = 0
        self.tile_offset_y = 0

    def get_player_input(self):
        keys = pygame.key.get_pressed()
        
        scroll_speed = 0.2#controls how fast world scrolls, could change this based on if in water or not
        
        dx, dy = 0,0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        if dx != 0 and dy != 0: #uses pythagorean theorem to "normalize" diagonal movement 
            dx *= 0.7071
            dy *= 0.7071

        self.scroll_x_float += dx *scroll_speed
        self.scroll_y_float +=dy *scroll_speed

        self.scroll_x_float = max(0, min(self.scroll_x_max, self.scroll_x_float))
        self.scroll_y_float = max(0, min(self.scroll_y_max, self.scroll_y_float))
        
        self.scroll_x = int(self.scroll_x_float) #int truncates down
        self.scroll_y = int(self.scroll_y_float)
        
        self.tile_offset_x = self.scroll_x_float %1 * Biomes.tile_size #get number of pixels offsetted, to prevent jerkiness when moving diagonally
        self.tile_offset_y = self.scroll_y_float %1 *Biomes.tile_size


    def render_images(self):

        for y in range (Biomes.tile_height):
            for x in range (Biomes.tile_width):
                if self.biome_map[self.scroll_y+y,self.scroll_x +x] == 0: 
                    continue #skips this if statement, the tile is meant to be a water square
                else:
                    draw_x = x* Biomes.tile_size - self.tile_offset_x
                    draw_y = y* Biomes.tile_size - self.tile_offset_y                   
                    
                    scaled_texture_surf = Biomes.BIOME_TEXTURES[self.biome_map[self.scroll_y +y ,self.scroll_x +x]]  
                    self.background.blit(scaled_texture_surf, (draw_x, draw_y))
   
    def render_water(self, screen):

        for y in range (Biomes.tile_height):
            for x in range (Biomes.tile_width):     
                if self.biome_map[self.scroll_y + y,self.scroll_x +x] == 0: 
                    draw_x = x* Biomes.tile_size - self.tile_offset_x
                    draw_y = y* Biomes.tile_size - self.tile_offset_y 
                    
                    scaled_texture_surf = Biomes.BIOME_TEXTURES[self.biome_map[self.scroll_y +y,self.scroll_x +x]][int(self.water_index)]    
                    screen.blit(scaled_texture_surf, (draw_x, draw_y))
        

    def draw_world(self, screen):
        self.get_player_input()
        self.render_images()
        screen.blit(self.background, (0,0))

# def load_and_prep_player_image(path):
#     image = pygame.image.load(path).convert()
#     image = pygame.transform.scale(image, (64,64))
#     image.set_colorkey((109,170,44)) 
#     return image

class Player(pygame.sprite.Sprite):
    
    player_stills = {
        'west'  : load_and_prep_player_image('graphics/player/player_still_west.png', (64,64)), 
        'east'  : load_and_prep_player_image('graphics/player/player_still_east.png', (64,64)), 
        'north' : load_and_prep_player_image('graphics/player/player_still_north.png', (64,64)), 
        'south' : load_and_prep_player_image('graphics/player/player_still_south.png', (64,64)) 
    }
    player_walks = {
        'west' : [load_and_prep_player_image('graphics/player/player_walks_west1.png', (64,64)) , load_and_prep_player_image('graphics/player/player_walks_west2.png', (64,64)) ],
        'east' : [load_and_prep_player_image('graphics/player/player_walks_east1.png', (64,64)) , load_and_prep_player_image('graphics/player/player_walks_east2.png', (64,64)) ],
        'north': [load_and_prep_player_image('graphics/player/player_walks_north1.png', (64,64)) , load_and_prep_player_image('graphics/player/player_walks_north2.png', (64,64)) ],
        'south': [load_and_prep_player_image('graphics/player/player_walks_south1.png', (64,64)) , load_and_prep_player_image('graphics/player/player_walks_south2.png', (64,64)) ]
    }

    def __init__(self):
        super().__init__()
        
        self.health = 10 #num of hearts player gets
        self.full_heart = load_and_prep_player_image('graphics/player/full_heart.png', (48,48))
        self.half_heart = load_and_prep_player_image('graphics/player/half_heart.png', (48,48))     

        self.walk_index = 0
        self.direction = 'south'

        self.image = Player.player_stills[self.direction] #just the initial surface, this will change later
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height/2))
    
       

    def find__and_draw_health(self, screen): #don't put this into update() method because it's drawing, not logic
        if collision():
            self.health -= 0.5 
        

    def animation_state(self): #standing, walking, swimming, getting hit, etc.
        keys = pygame.key.get_pressed()
        
        self.walk_index += 0.1
        if self.walk_index >= 2: self.walk_index = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.image = Player.player_walks['west'][int(self.walk_index)]
            self.direction = 'west'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.image = Player.player_walks['east'][int(self.walk_index)]
            self.direction = 'east'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = Player.player_walks['north'][int(self.walk_index)]
            self.direction = 'north'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = Player.player_walks['south'][int(self.walk_index)]
            self.direction = 'south'
        else: #no buttons are pressed
            self.image = Player.player_stills[self.direction]


    def update(self):
        self.animation_state()


# def collision():
#     if pygame.sprite.spritecollide(player.sprite, mob_group, False):
#         return True
#     else: return False

world = Biomes()

#Groups
player = Player() #create a Player() sprite
player_group = pygame.sprite.GroupSingle(player) #add the sprite to the GroupSingle group

# player_group= pygame.sprite.GroupSingle() #creates an empty GroupSingle Instance
# player_group.add(Player()) #adds a single Player() sprite instance to the GroupSingle group called player

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
    

    #Player
    player.update() #calls the update() method for player
    player_group.draw(screen) #draws player sprite .image at its .rect

    #Hostile Mobs
    #mob_group.update() #calls the update() method for each enemy instance
    #mob_group.draw(screen) #goes through every sprite in the group and draws their .image at their .rect

    screen.blit(player.half_heart, (30,30))
    screen.blit(player.full_heart, (70,70))


    pygame.display.update() 
    clock.tick(60)
