import pygame

def load_and_prep_player_image(path, size):
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size)
    image.set_colorkey((109,170,44)) 
    return image