import pygame
from sys import exit
from random import randint, choice
from map_generator import generate_biome_map
from utils import load_and_prep_player_image


SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1280  #make sure TILE_SIZE multiplies into these cleanly
BIOME_MAP_SCALAR =4 #biome_map will be x times as large as regular map, to allow scrolling background
TILE_SIZE = 32
SCREEN_WIDTH_TILES = SCREEN_WIDTH //TILE_SIZE #width of the visible screen, in tiles
SCREEN_HEIGHT_TILES = SCREEN_HEIGHT //TILE_SIZE


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minecraft 2D')
clock = pygame.time.Clock()
game_state = 0 #starts in world creation screen
game_font_large = pygame.font.Font('font/minecraft_font.ttf', 100)
game_font_medium = pygame.font.Font('font/minecraft_font.ttf', 30)
game_font_small = pygame.font.Font('font/minecraft_font.ttf', 22)


# Things to do?
# change forest block to be nicer
# add swimming animation
# Add plants to biomes
# Add mobs (friendly and hostile), have them spawn according to timed unique event
# add enemy damage to health, and combat
# Add sound fx and music



#plains, desert, water, snow, mountain, forest
class Biomes(): #making it inherit from sprite class is overkill unless I want to make each specific tile interactable with the player


    BIOME_TEXTURES = { #these don't match or make sense rn, change later
        0: [pygame.transform.scale(pygame.image.load('graphics/water/deep_water_1.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)), pygame.transform.scale(pygame.image.load('graphics/water/deep_water_2.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) ],   # Deep Water, want to alternate between these two
        1: pygame.transform.scale(pygame.image.load('graphics/blocks/desert_block.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),   # Desert
        2: pygame.transform.scale(pygame.image.load('graphics/blocks/grass_top.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),      # Grassland
        3: pygame.transform.scale(pygame.image.load('graphics/blocks/maple_leaves.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),     # Forest
        4: pygame.transform.scale(pygame.image.load('graphics/blocks/stone_generic.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)), # Mountain
        5: pygame.transform.scale(pygame.image.load('graphics/blocks/snow.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) #Snow
    }
    
    def __init__(self, seed):
        self.resolution_scale = 3200//TILE_SIZE #make this larger to see smoother/larger biome regions
        self.water_index = 0
        
        self.biome_map = generate_biome_map(BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES,BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES, seed, self.resolution_scale)#returns 2D NumPy array filled with integers 0 to 5 representing biomes
        self.static_background =  self.create_static_layer()    
        
        self.static_background_draw_x = -(int(0.5 *(BIOME_MAP_SCALAR * SCREEN_WIDTH - SCREEN_WIDTH) / TILE_SIZE)) #in tiles
        self.static_background_draw_y = -(int(0.5 *(BIOME_MAP_SCALAR * SCREEN_HEIGHT - SCREEN_HEIGHT) / TILE_SIZE))
        self.static_background_draw_x_min = -(BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES - SCREEN_WIDTH_TILES) +1
        self.static_background_draw_y_min = -(BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES - SCREEN_HEIGHT_TILES) +1
    

        #scroll_x should always be on left edge of vsisible game screen, scroll_y on the top edge of visible game screen
        self.scroll_x = int(0.5 *(BIOME_MAP_SCALAR * SCREEN_WIDTH - SCREEN_WIDTH) / TILE_SIZE) #calculates scroll_x 
        self.scroll_y = int(0.5 *(BIOME_MAP_SCALAR * SCREEN_HEIGHT - SCREEN_HEIGHT) / TILE_SIZE) #calculates scroll_y

        self.scroll_x_max = BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES - SCREEN_WIDTH_TILES - 1 # max of how far the player can explore
        self.scroll_y_max = BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES - SCREEN_HEIGHT_TILES - 1 # minus one accounts for the extra 1 tile of perimeter width and height
        
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

        self.static_background_draw_x -= dx * scroll_speed # for controlling static terrain
        self.static_background_draw_y -= dy * scroll_speed # 

        self.static_background_draw_x = min(0, max(self.static_background_draw_x, self.static_background_draw_x_min)) 
        self.static_background_draw_y = min(0, max(self.static_background_draw_y, self.static_background_draw_y_min))

        self.scroll_x_float += dx *scroll_speed #for controlling changing terrain(water)
        self.scroll_y_float +=dy *scroll_speed

        self.scroll_x_float = max(0, min(self.scroll_x_max, self.scroll_x_float)) 
        self.scroll_y_float = max(0, min(self.scroll_y_max, self.scroll_y_float)) 
        
        self.scroll_x = int(self.scroll_x_float) #int truncates down
        self.scroll_y = int(self.scroll_y_float)
        
        self.tile_offset_x = self.scroll_x_float %1 * TILE_SIZE #get number of pixels offsetted, to prevent jerkiness when moving diagonally
        self.tile_offset_y = self.scroll_y_float %1 *TILE_SIZE

    def create_static_layer(self):
        #no need for offsetting for blur, as the background is already completely rendered
        static_background = pygame.Surface((BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES* TILE_SIZE, BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES * TILE_SIZE))
        
        for y in range (BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES):
            for x in range(BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES):
                
                

                biome_id = self.biome_map[y, x]
                
                if biome_id == 0:
                    continue
                else: 
                    scaled_texture_surf = Biomes.BIOME_TEXTURES[biome_id]
                    static_background.blit(scaled_texture_surf, (x * TILE_SIZE,y * TILE_SIZE))
        return static_background

    def render_static_layer(self, screen): 
        screen.blit(self.static_background, (self.static_background_draw_x * TILE_SIZE, self.static_background_draw_y * TILE_SIZE))


    def render_water(self, screen):
        perimeter_size = 1 #means one tile of space all around visible screen

        for y in range (SCREEN_HEIGHT_TILES + 2 *perimeter_size ):
            for x in range (SCREEN_WIDTH_TILES + 2 *perimeter_size):     
                biome_id = self.biome_map[self.scroll_y+y - perimeter_size ,self.scroll_x +x - perimeter_size ]

                draw_x = (x - perimeter_size) * TILE_SIZE  - self.tile_offset_x
                draw_y = (y - perimeter_size) * TILE_SIZE - self.tile_offset_y 

            
                if biome_id == 0: 

                    scaled_texture_surf = Biomes.BIOME_TEXTURES[biome_id][int(self.water_index)]    
                    screen.blit(scaled_texture_surf, (draw_x, draw_y))
        

    def draw_world(self, screen):
        self.get_player_input()
        self.render_static_layer(screen)
        self.render_water(screen)



class Player(pygame.sprite.Sprite):
    
    player_stills = {
        'west'  : load_and_prep_player_image('graphics/player/player_still_west.png', (64,64), (109,170,44)), 
        'east'  : load_and_prep_player_image('graphics/player/player_still_east.png', (64,64), (109,170,44)), 
        'north' : load_and_prep_player_image('graphics/player/player_still_north.png', (64,64), (109,170,44)), 
        'south' : load_and_prep_player_image('graphics/player/player_still_south.png', (64,64), (109,170,44)) 
    }
    player_walks = {
        'west' : [load_and_prep_player_image('graphics/player/player_walks_west1.png', (64,64), (109,170,44)) , load_and_prep_player_image('graphics/player/player_walks_west2.png', (64,64), (109,170,44)) ],
        'east' : [load_and_prep_player_image('graphics/player/player_walks_east1.png', (64,64), (109,170,44)) , load_and_prep_player_image('graphics/player/player_walks_east2.png', (64,64), (109,170,44)) ],
        'north': [load_and_prep_player_image('graphics/player/player_walks_north1.png', (64,64), (109,170,44)) , load_and_prep_player_image('graphics/player/player_walks_north2.png', (64,64), (109,170,44)) ],
        'south': [load_and_prep_player_image('graphics/player/player_walks_south1.png', (64,64), (109,170,44)) , load_and_prep_player_image('graphics/player/player_walks_south2.png', (64,64), (109,170,44)) ]
    }

    def __init__(self):
        super().__init__()
        
        self.health = 10 #num of hearts player gets
        self.full_heart = load_and_prep_player_image('graphics/player/full_heart.png', (48,48), (109,170,44))
        self.half_heart = load_and_prep_player_image('graphics/player/half_heart.png', (48,48), (109,170,44))     

        self.walk_index = 0
        self.direction = 'south'

        self.image = Player.player_stills[self.direction] #just the initial surface, this will change later
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def find_and_draw_health(self, screen): #
        if is_collision():
            self.health -= 0.5 
        
        num_full_hearts = int(self.health)
        for i in range(num_full_hearts):
            screen.blit(player.full_heart, (30 + 40*i, 25))

        if not self.health.is_integer(): # 9.0 is considered an integer
            screen.blit(player.half_heart, (30 + 40 * num_full_hearts, 25))
        

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

class Hostile_mob(pygame.sprite.Sprite):
    spawn_radius = (SCREEN_WIDTH_TILES //2)+ 24
    mob_images = {
        'zombie' : load_and_prep_player_image('graphics/hostile_mobs/zombie/zombie_idle.png', (128,128), (147, 187, 236))
    }


    def __init__(self, type):
        super().__init__()
        
        spawn_x, spawn_y = Hostile_mob.random_spawn_pos() #in tiles, randomly generate this based on spawn_radius
        
        self.true_x = spawn_x + (BIOME_MAP_SCALAR * SCREEN_WIDTH_TILES - SCREEN_WIDTH_TILES)//2
        self.true_y = spawn_y + (BIOME_MAP_SCALAR * SCREEN_HEIGHT_TILES - SCREEN_HEIGHT_TILES)//2

        self.image = Hostile_mob.mob_images[type]
        self.rect = self.image.get_rect() #place holder 

    def chase_player(self):
   
        true_player_x = world.scroll_x_float + SCREEN_WIDTH_TILES //2
        true_player_y = world.scroll_y_float + SCREEN_HEIGHT_TILES //2

        dx = true_player_x - self.true_x - 64/TILE_SIZE
        dy = true_player_y - self.true_y - 64/TILE_SIZE

        distance = (dx**2 + dy**2) **0.5 # creates vector for zombie to follow to the player
        if distance != 0:
            dx /= distance
            dy /= distance

        
        speed = 0.05    
        self.true_x += dx * speed
        self.true_y += dy * speed

    def update_rect(self): #
        self.rect.topleft = ((self.true_x - world.scroll_x_float) * TILE_SIZE, (self.true_y - world.scroll_y_float) * TILE_SIZE)


    @staticmethod
    def random_spawn_pos():
        random_x = randint(-Hostile_mob.spawn_radius, Hostile_mob.spawn_radius)
        random_y = randint(-Hostile_mob.spawn_radius, Hostile_mob.spawn_radius)
        x = SCREEN_WIDTH_TILES//2 + random_x
        y = SCREEN_HEIGHT_TILES//2 + random_y
        return x , y


    def update(self):
        self.chase_player()
        self.update_rect()


def is_collision():
    if pygame.sprite.spritecollide(player, hostile_mobs, False):
        return True
    else: return False


#Game state == 2
game_over = game_font_large.render('GAME OVER', False, (222,4,4))
game_over_rect = game_over.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

#Game state == 0
gray = (128,128,128)
black =(0,0,0)
white = (235,235,235)

start_up_background = pygame.image.load('graphics/startup_screen_background.png').convert_alpha()
start_up_background_rect = start_up_background.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
# start_up_background_width, start_up_background_height = start_up_background.get_size()

create_new_world = game_font_medium.render(('Create New World'), False, white)
create_new_world_rect = create_new_world.get_rect(center = (SCREEN_WIDTH/2, 450))
message1 = game_font_small.render(('Seed for the World Generator'), False, gray)
message1_rect = message1.get_rect(midleft = (SCREEN_WIDTH/2 - 244, SCREEN_HEIGHT/2 +76))
message2 = game_font_small.render('Leave blank for a random seed', False, gray)
message2_rect = message2.get_rect(midleft = (SCREEN_WIDTH/2 - 244, SCREEN_HEIGHT/2 + 164))
seed_str = ''
cursor_visible = True
seed_max = 1000000
seed_min = 0



#Background
world = None

#Groups
player = Player() #create a Player() sprite
player_group = pygame.sprite.GroupSingle(player) #add the sprite to the GroupSingle group

hostile_mobs = pygame.sprite.Group() #creates an empty "bucket" that holds sprites

#Ttimers
mob_spawn_event = pygame.USEREVENT + 1 #creates custom user event with unique int
pygame.time.set_timer(mob_spawn_event, 4000) #pushes mob spawn event onto list every 5 seconds

cursor_blink = pygame.USEREVENT + 2 
pygame.time.set_timer(cursor_blink, 500)

game_over_reset = pygame.USEREVENT + 3



last_updated_time = pygame.time.get_ticks()
while True:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            pygame.quit() 
            exit() 

        if game_state == 0: #create world screen
            if event.type == cursor_blink:
                cursor_visible = not cursor_visible
            
            if event.type == pygame.KEYDOWN: #doing this makes sure only one character typed at a time (of same character )
                if event.unicode.isdigit(): # event.unicode returns string representation (a single character) of key that was pressed for example 'a' or '9, isdigit() is a Python method that checks if all characters in string are digits (0-9)
                    seed_str += event.unicode
    
                elif event.key == pygame.K_BACKSPACE: 
                    seed_str = seed_str[ : -1]
                
                if event.key == pygame.K_RETURN: 
                    if len(seed_str) ==0: #checks if player has left the seed blank
                        seed = randint(0,seed_max)
                    else:
                        seed = int(seed_str)
                        seed = max(seed_min, min(seed, seed_max))
                    
                    print("Seed:", seed)
                    world = Biomes(seed) #initialize world once I have the seed
                    game_state = 1
                    seed_str = '' #resets seed_str for next time
        
        if game_state == 1:
    
            if event.type == mob_spawn_event:
                for i in range(3):
                    hostile_mobs.add(Hostile_mob(choice(['zombie', 'zombie']))) #add different mobs later

        if game_state == 2:
            if event.type == game_over_reset:
                game_state = 0
                pygame.time.set_timer(game_over_reset, 0) #tells pygame to stop sending this timer event
                     

    if game_state == 0: #create new world screen
        #Background
        screen.fill((0,0,0))
        screen.blit(start_up_background, start_up_background_rect)
        
        #Text
        screen.blit(create_new_world, create_new_world_rect) #text
        screen.blit(message1, message1_rect) #text
        screen.blit(message2, message2_rect) #text
        
        #Outlined box
        draw_rect_x = SCREEN_WIDTH/2 - 250
        draw_rect_y = SCREEN_HEIGHT/2 + 90
        pygame.draw.rect(screen, black, (draw_rect_x , draw_rect_y, 500, 60))        
        pygame.draw.rect(screen, gray, (draw_rect_x , draw_rect_y, 500, 60), 3)

        #Display seed text
        display_str = seed_str + ('_' if cursor_visible else '') 
        seed_text = game_font_small.render(display_str, False, white)
        seed_text_rect = seed_text.get_rect(midleft = ( SCREEN_WIDTH/2 - 240 , SCREEN_HEIGHT/2 + 120 ))
        screen.blit(seed_text, seed_text_rect)

    elif game_state == 1: #game active screen
        # Background
        world.water_index += 0.015 
        if world.water_index > len(Biomes.BIOME_TEXTURES[0]): world.water_index = 0
        world.draw_world(screen)
    
        #Hostile Mobs
        hostile_mobs.update() #calls the update() method for each enemy instance
        hostile_mobs.draw(screen) #goes through every sprite in the group and draws their .image at their .rect

        #Player
        player.find_and_draw_health(screen) #processes damage, and draws health
        player.update() #calls the update() method for player
        player_group.draw(screen) #draws player sprite .image at its .rect
        if player.health <= 0:
            game_state = 2
            pygame.time.set_timer(game_over_reset, 5000, 1)
            player.health = 10 #reset health
            hostile_mobs.empty()

        



    elif game_state == 2: #game over screen
        
        screen.fill((0,0,0))
        screen.blit(game_over, game_over_rect)



    pygame.display.update() 
    clock.tick(60)
