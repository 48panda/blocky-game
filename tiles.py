import pygame
import numpy as np
import colorsys
from PIL import Image

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b = np.rollaxis(pygame.surfarray.array3d(arr).swapaxes(0,1), axis=-1)
    a = pygame.surfarray.array_alpha(arr).swapaxes(0,1)
    h, s, v = rgb_to_hsv(r, g, b)
    h += hout
    r, g, b = hsv_to_rgb(h, s, v)
    im = Image.fromarray(np.dstack((r, g, b, a)))
    mode = im.mode
    size = im.size
    data = im.tobytes()  
    return pygame.image.fromstring(data, size, mode)
class tile:
    player_collide = False
    player_stand = True
    texture = None
    def stand(renderer):
        pass
class wall(tile):
    texture = pygame.image.load("assets/tiles/wall.png")
    player_collide = True
class floor(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
class tileGoal(tile):
    texture = pygame.image.load("assets/tiles/tilegoal.png")
class buttonRed(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/button.png"),0),(0,0))
    def stand(renderer):
        for y, row in enumerate(renderer.world):
            for x, cell in enumerate(row):
                if cell == laserVRed or cell == laserHRed:
                    renderer.world[y][x] = floor
class laserVRed(tile):
    player_collide = True
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/laser.png"),0),(0,0))
class laserHRed(tile):
    player_collide = True
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/laser.png"),0),(0,0))
    texture = pygame.transform.rotate(texture, 90)
class buttonGreen(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/button.png"),0.333),(0,0))
    def stand(renderer):
        for y, row in enumerate(renderer.world):
            for x, cell in enumerate(row):
                if cell == laserVGreen or cell == laserHGreen:
                    renderer.world[y][x] = floor
class laserVGreen(tile):
    player_collide = True
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/laser.png"),0.333),(0,0))
class laserHGreen(tile):
    player_collide = True
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/laser.png"),0.333),(0,0))
    texture = pygame.transform.rotate(texture, 90)
class portalOrange(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/portal.png"),0),(0,0))
    def stand(renderer):
        if renderer.hasTeleported:
            return
        renderer.hasTeleported = True
        done = False
        for y, row in enumerate(renderer.world):
            for x, cell in enumerate(row):
                if cell == portalOrange:
                    if renderer.player_x != x and renderer.player_y != y:
                        renderer.player_x = x
                        renderer.player_y = y
                        done = True
                        break
            if done:
                break
class portalBlue(tile):
    texture = pygame.image.load("assets/tiles/floor.png")
    texture.blit(shift_hue(pygame.image.load("assets/tiles/portal.png"),0.7),(0,0))
    def stand(renderer):
        if renderer.hasTeleported:
            return
        renderer.hasTeleported = True
        done = False
        for y, row in enumerate(renderer.world):
            for x, cell in enumerate(row):
                if cell == portalBlue:
                    if renderer.player_x != x and renderer.player_y != y:
                        renderer.player_x = x
                        renderer.player_y = y
                        done = True
                        break
            if done:
                break
class hole(tile):
    player_stand = False
    texture = pygame.image.load("assets/tiles/hole.png")

tile_key = {"wall":wall, "floor":floor, "hole":hole, "buttonRed":buttonRed, "laserVRed":laserVRed, "laserHRed":laserHRed,
 "buttonGreen":buttonGreen, "laserVGreen":laserVGreen, "laserHGreen":laserHGreen,
 "portalOrange":portalOrange, "portalBlue":portalBlue,
 "tileGoal":tileGoal}