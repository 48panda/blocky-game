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

tile_key = {"wall":wall, "floor":floor}