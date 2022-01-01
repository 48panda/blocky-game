import pygame
class tile:
    player_collide = False
    player_stand = True
    texture = None

class wall(tile):
    texture = pygame.image.load("assets/tiles/wall.png")
    player_collide = True
class floor(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
class hole(tile):
    player_stand = False
    texture = pygame.image.load("assets/tiles/hole.png")

tile_key = {"wall":wall, "floor":floor, "hole":hole}