import pygame
#for storing and initiliazing variables/objects/rects/text etc from starting screen


#####outside main game loop, intializing stuff

def set_colors():
    gray = (128,128,128)
    black =(0,0,0)
    white = (235,235,235)   
    
    return gray, black, white

def set_background(SCREEN_WIDTH, SCREEN_HEIGHT):
    start_up_background = pygame.image.load('graphics/startup_screen_background.png').convert_alpha()
    start_up_background_rect = start_up_background.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    return start_up_background, start_up_background_rect

def set_texts(game_font_small, game_font_medium, SCREEN_WIDTH, SCREEN_HEIGHT, white, gray):
    create_new_world = game_font_medium.render(('Create New World'), False, white)
    create_new_world_rect = create_new_world.get_rect(center = (SCREEN_WIDTH/2, 450))
    
    message1 = game_font_small.render(('Seed for the World Generator'), False, gray)
    message1_rect = message1.get_rect(midleft = (SCREEN_WIDTH/2 - 244, SCREEN_HEIGHT/2 +76))
    
    message2 = game_font_small.render('Leave blank for a random seed', False, gray)
    message2_rect = message2.get_rect(midleft = (SCREEN_WIDTH/2 - 244, SCREEN_HEIGHT/2 + 164))
    
    return create_new_world, create_new_world_rect, message1, message1_rect, message2, message2_rect

def set_underscore():
    seed_str = ''
    cursor_visible = True
    seed_max = 1000000
    seed_min = 0
    return seed_str, cursor_visible, seed_max, seed_min

######inside main game loop

def draw_background(screen, start_up_background, start_up_background_rect): #dirt screen
    screen.fill((0,0,0))
    screen.blit(start_up_background, start_up_background_rect)

def draw_text(screen, create_new_world, create_new_world_rect, message1, message1_rect, message2, message2_rect):
    screen.blit(create_new_world, create_new_world_rect)
    screen.blit(message1, message1_rect) 
    screen.blit(message2, message2_rect)

def draw_outline(screen, SCREEN_WIDTH, SCREEN_HEIGHT, black, gray):
    draw_rect_x = SCREEN_WIDTH/2 - 250
    draw_rect_y = SCREEN_HEIGHT/2 + 90
    pygame.draw.rect(screen, black, (draw_rect_x , draw_rect_y, 500, 60))        
    pygame.draw.rect(screen, gray, (draw_rect_x , draw_rect_y, 500, 60), 3)

def draw_seed_text(screen, seed_str, game_font_small, white, cursor_visible, SCREEN_WIDTH, SCREEN_HEIGHT):
    display_str = seed_str + ('_' if cursor_visible else '') 
    seed_text = game_font_small.render(display_str, False, white)
    seed_text_rect = seed_text.get_rect(midleft = ( SCREEN_WIDTH/2 - 240 , SCREEN_HEIGHT/2 + 120 ))
    screen.blit(seed_text, seed_text_rect)