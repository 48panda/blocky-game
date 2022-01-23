import pygame
import json
from pygame import gfxdraw
from level_runner import play_level
from itertools import count, filterfalse
import os
import pickle
import colorsys

def saturateRGB(color, saturateAmount):
    return (min(255, max(0, color[0] * saturateAmount)), min(255, max(0, color[1] * saturateAmount)), min(255, max(0, color[2] * saturateAmount)))

with open("levels.json") as f:
    levels = json.load(f)["levels"]
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

pygame.font.init()
font = pygame.font.SysFont("Arial", 80,bold=1)
font2 = pygame.font.SysFont("Calibri", 60,bold=1)
font3 = pygame.font.SysFont("Calibri", 30, bold=1)
def render_multi_line(text, x, y,):
    text = text.splitlines()
    for i, l in enumerate(text):
        screen.blit(font3.render(l, 0, (255,255,255)), (x, y + 30*i))
def draw_level(index,x,y,completed_levels,hover, render = True, screen=screen):
    centers = {index:(x,y)}
    color = saturateRGB(colorsys.hsv_to_rgb(levels[index]["color"], 0.8, 0.6),255)
    if index == hover:
        color = saturateRGB(color, 2)
    forkdir = levels[index]["fork"]
    if forkdir == "center":
        new_y = y + 100 * (len(levels[index]["children"]) - 1)
    else:
        new_y = y
    new_x = x + 200
    if index in completed_levels:
        for lvl in levels[index]["children"]:
            
            if render:
                pygame.draw.line(screen,(0,0,0),(x,y),(x+100,y),10)
                pygame.draw.line(screen,(0,0,0),(x+100,y),(new_x,new_y),10)
            centers.update(draw_level(lvl,new_x,new_y,completed_levels,hover, render = render, screen=screen))
            if forkdir == "down":
                new_y += 200
            else:
                new_y -= 200

    if render:
        pygame.gfxdraw.aacircle(screen,x,y,50,color)
        pygame.gfxdraw.filled_circle(screen,x,y,50,color)
    circle_center = (x,y)
    text = font.render(str(index+1).zfill(2), True, saturateRGB(color,0.5))
    text_size = text.get_size()
    screen.blit(text, (circle_center[0]-text_size[0]//2,circle_center[1]-text_size[1]//2))
    new_x = x + 200
    new_y = y
    return centers
def render_circles_to_surface(completed,hover,x,y):
    circle_centers = draw_level(0, 0, 0, completed, hover, render=False)
    xmax,ymax = tuple(max(i) for i in zip(*circle_centers.values()))
    xmin,ymin = tuple(min(i) for i in zip(*circle_centers.values()))
    level_selector_surface = pygame.Surface((xmax-xmin+100,ymax-ymin+100), pygame.SRCALPHA, 32)
    draw_level(0, 50-xmin, 50-ymin, completed, hover, screen=level_selector_surface)
    return level_selector_surface, {k:(pos[0] + x + 50, pos[1] + y +50 - ymin) for k,pos in circle_centers.items()}

def get_height(index,completed_levels):
    height = 200
    if index in completed_levels:
        height += max([get_height(lvl,completed_levels) for lvl in levels[index]["children"]])
    return height
if os.path.isfile("player_data/completed"):
    with open("player_data/completed", "rb") as f:
        completed = pickle.load(f)
        assert type(completed) == list, "Error with data, to fix please delete player_data/completed"
        for i in completed:
            assert type(i) == int , "Error with data, to fix please delete player_data/completed"
else:
    completed = []
center_circles = {}
running = True
hover = None
click = min(next(filterfalse(set(completed).__contains__, count(0))),len(levels)-1)
hover_play_button = False
play_button = font.render("PLAY", True, (33, 255, 151), saturateRGB((33, 255, 151), 0.5))
play_button_saturated = font.render("PLAY", True, saturateRGB((33, 255, 151), 1.2), saturateRGB((33, 255, 151), 0.5*1.2))
play_button_size = play_button.get_size()
play_button_pos = (screen.get_width()-play_button_size[0]-20,250-play_button_size[1]-20)
play_button_rect = pygame.Rect(play_button_pos[0],play_button_pos[1],play_button_size[0],play_button_size[1])
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                found_click = False
                for i,pos in center_circles.items():
                    x,y = pos
                    distance = (x-event.pos[0])**2 + (y-event.pos[1])**2
                    if distance < 2500:
                        click = i
                        found_click = True
                        break
                if play_button_rect.collidepoint(event.pos):
                    running, won = play_level(click)
                    if not running:
                        break
                    if won:
                        if click not in completed:
                            completed.append(click)
                            click = min(next(filterfalse(set(completed).__contains__, count(0))),len(levels)-1)
                            with open("player_data/completed", "wb") as f:
                                pickle.dump(completed,f)
    screen.fill((255,255,255))
    for i,pos in center_circles.items():
        x,y = pos
        mouse_pos = pygame.mouse.get_pos()
        distance = (x-mouse_pos[0])**2 + (y-mouse_pos[1])**2
        if distance < 2500:
            hover = i
        else:
            if hover == i:
                hover = None
    mouse_pos = pygame.mouse.get_pos()
    selected = None
    if click is None:
        selected = hover
    else:
        selected = click
    hover_play_button = selected!=None and play_button_rect.collidepoint(mouse_pos)
    x_offset = 200
    y_offset = screen.get_height()//2
    level_selector_surface, center_circles = render_circles_to_surface(completed,selected,x_offset,y_offset)
    screen.blit(level_selector_surface, (x_offset,y_offset))
    if selected is not None:
        pygame.draw.rect(screen,(100,100,100),(0,0,screen.get_width(),250))
        if hover_play_button:
            screen.blit(play_button_saturated, play_button_pos)
        else:
            screen.blit(play_button, play_button_pos)
        text = font2.render(levels[selected]["name"], True, (255,255,255))
        screen.blit(text, (10,10))
        render_multi_line(levels[selected]["desc"], 10, 70)
    pygame.display.flip()
