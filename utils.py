import pygame

def load_and_prep_player_image(path, size, colorkey):
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey) 
    return image

def is_collision(player, hostile_mobs): #checks if player has collided with hostile_mobs
    if pygame.sprite.spritecollide(player, hostile_mobs, False):
        return True
    else: return False