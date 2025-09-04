import pygame

def load_and_prep_player_image(path, size, colorkey):
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey) 
    return image