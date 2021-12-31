import pygame
import json
from pygame import gfxdraw
from level_runner import play_level

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
def draw_level(index,x,y,completed_levels,hover):
    centers = {index:(x,y)}
    color = levels[index]["color"]
    if index == hover:
        color = saturateRGB(color, 2)
    pygame.gfxdraw.aacircle(screen,x,y,50,color)
    pygame.gfxdraw.filled_circle(screen,x,y,50,color)
    circle_center = (x,y)
    text = font.render(str(index+1).zfill(2), True, saturateRGB(color,0.5))
    text_size = text.get_size()
    screen.blit(text, (circle_center[0]-text_size[0]/2,circle_center[1]-text_size[1]/2))
    new_x = x
    new_y = y - 200
    if index in completed_levels:
        for lvl in levels[index]["children"]:
            centers.update(draw_level(lvl,new_x,new_y,completed_levels,hover))
            new_x += 200
    return centers
def get_height(index,completed_levels):
    height = 200
    if index in completed_levels:
        height += max([get_height(lvl,completed_levels) for lvl in levels[index]["children"]])
    return height
completed = []
center_circles = {}
running = True
hover = None
click = None
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
                if not found_click and event.pos[1]>250:
                    click = None
                    break
                if play_button_rect.collidepoint(event.pos):
                    running, won = play_level(click)
                    if not running:
                        break
                    if won:
                        if click not in completed:
                            completed.append(click)
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
    center_circles = draw_level(0,screen.get_width()//2,screen.get_height()-200,completed,selected)
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