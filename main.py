import program_renderer
import pygame
import blocks
import runner
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.font.init()
program = [blocks.ifBlock("player_x > player_y"),blocks.ifBlock("player_y > 0"),blocks.printBlock("e"),blocks.waitBlock(2),blocks.endifBlock(),blocks.endifBlock(),blocks.jumpBlock(0)]
renderer = program_renderer.renderer(screen, program, (0,0), runner.Runner)
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