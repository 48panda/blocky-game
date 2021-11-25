import pygame
import player_render as player
game = pygame.display.set_mode((1920//2, 1080//2))
#game = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
mainLoop = True
angle = 0
while mainLoop:
    angle += 0
    game.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    player.render(game,(0,0),angle,0,0,0,0,0,0,0,0,0)
    pygame.display.update()

pygame.quit()
