import pygame
import random
from platformer.render_functions import *
import grid.main

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.font.init()

loading_screen = pygame.image.load("assets/loadingscreen.png")

font = pygame.font.SysFont("Arial", 60)
with open("assets/loadingscreen.txt", "r") as f:
    text = f.readlines()
text = random.choice(text)
text = text.rstrip().lstrip()
text = font.render(text, True, (255,255,255))
text_width, text_height = text.get_size()
position_to_render_text = (screen.get_width()//2 - text_width//2, screen.get_height()//(1/0.8) - text_height)
clock = pygame.time.Clock()

position = 0

time_since_last_change = 0

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.blit(loading_screen, (0,0))
    time = clock.tick(60)
    time_since_last_change += time
    if time_since_last_change > 100:
        position += random.random() / 20
        time_since_last_change = 0
    if position > 1:
        break
    box(screen,(-0.5,0.3),(1,0.1),(0,0,0))
    box(screen,(-0.5,0.3),(position,0.1),(0,0,255))
    screen.blit(text, position_to_render_text)
    pygame.display.update()
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    