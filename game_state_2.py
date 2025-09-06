
import pygame


#initial variables
def set_game_over(game_font_large, SCREEN_WIDTH, SCREEN_HEIGHT):
    game_over = game_font_large.render('GAME OVER', False, (222,4,4))
    game_over_rect = game_over.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    return game_over, game_over_rect



# in main game loop
def show_game_over(screen, game_over, game_over_rect):
    screen.fill((0,0,0))
    screen.blit(game_over, game_over_rect)