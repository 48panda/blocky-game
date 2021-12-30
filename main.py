import grid_renderer
import pygame
import blocks
import runner
import json

with open("levels.json") as f:
    levels = json.load(f)["levels"]
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.font.init()
def play_function(button, playing):
    pass
level = levels[0]
def get_block_list_to_show(level):
    block_list_to_show = []
    for block in level["blocks"]:
        for b in blocks.blockList:
            if b.prefix == block:
                block_list_to_show.append(b)
                break
    return block_list_to_show

program = [blocks.moveBlock("right"),blocks.moveBlock("right"),blocks.moveBlock("down"),blocks.moveBlock("down"),blocks.moveBlock("left"),blocks.moveBlock("left")]
renderer = grid_renderer.grid_renderer(screen, program, (0,0), runner.Runner, blocks.blockList, get_block_list_to_show(level), world=level["data"])
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255,255,255))
    program = renderer.tick(events)
    pygame.display.flip()