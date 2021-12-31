import grid_renderer
import pygame
import blocks
import json

with open("levels.json") as f:
    levels = json.load(f)["levels"]
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.font.init()

def get_block_list_to_show(level):
    block_list_to_show = []
    for block in level["blocks"]:
        for b in blocks.blockList:
            if b.prefix == block:
                block_list_to_show.append(b)
                break
    return block_list_to_show

renderers = {"grid":grid_renderer.grid_renderer}

def play_level(level):
    level = levels[level]

    renderer = renderers[level["type"]](screen, blocks.blockList, get_block_list_to_show(level), data=level["data"])
    running = True
    won = False
    while running and not won:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((255,255,255))
        program, won = renderer.tick(events)
        pygame.display.flip()
    return running, won