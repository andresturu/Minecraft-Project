import pygame
from sys import exit
from random import randint, choice
from map_generator import generate_biome_map

screen_width, screen_height = 2*960 ,2 *640  #make sure tile_size multiplies into these cleanly
seed = randint(0,10000)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minecraft 2D')
clock = pygame.time.Clock()

# Things to do?
# have screen zoom in on part of the map, then it renders more as you walk further
# add enemy damage to health, and combat


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
        self.tile_size = 32
        tile_width = int(screen_width /self.tile_size) #for making the biome_map proportionally smaller
        tile_height = int(screen_height /self.tile_size)
        resolution_scale = int(1200/self.tile_size) #make this larger to see smoother/larger biome regions
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

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.health = 10 #num of hearts player gets
        self.full_heart = pygame.image.load('graphics/player/full_heart.png').convert() #not alpha becuase of transparency reasons
        self.full_heart = pygame.transform.scale(self.full_heart, (24,24) )
        self.full_heart.set_colorkey((109,170,44)) #sets background color to be transparent
        
        self.half_heart = pygame.image.load('graphics/player/half_heart.png').convert() #not alpha b/c transparency
        self.half_heart = pygame.transform.scale(self.half_heart, (24,24) )
        self.half_heart.set_colorkey((109,170,44)) 
        
        self.stand_still= pygame.image.load('graphics/player/player_still.png').convert() #not alpha
        self.stand_still = pygame.transform.scale(self.stand_still, (48,48) )
        self.stand_still.set_colorkey((109,170,44))         
    #     self.player_walk_1 =
    #     self.player_walk_2 =
    #     self.player_walk = [self.player_walk_1, self.player_walk_2]

        self.image = self.stand_still
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height/2))
    
    def do_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x +=2
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -=2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y  +=2
       

    def find__and_draw_health(self, screen): #don't put this into update() method because it's drawing, not logic
        if collision():
            self.health -= 0.5 
        

    # def animation_state(): #standing, walking, swimming, getting hit, etc.

    def update(self):
        self.do_movement()

def collision():
    if pygame.sprite.spritecollide(player.sprite, mob_group, False):
        return True
    else: return False

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
    #player.find_and_draw_health(screen)
    player.update() #calls the update() method for player
    player_group.draw(screen) #draws player sprite .image at its .rect

    #Hostile Mobs
    #mob_group.update() #calls the update() method for each enemy instance
    #mob_group.draw(screen) #goes through every sprite in the group and draws their .image at their .rect

    pygame.display.update() 
    clock.tick(60)