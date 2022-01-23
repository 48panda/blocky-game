import grid_renderer
import pygame
import blocks
import json
import pickle
import os
import itertools
class jumpIdGenerator:
            def __init__(self):
                self.value = 0
                self.change_next = True
            def __next__(self):
                if self.change_next:
                    self.value += 1
                self.change_next = not self.change_next
                return self.value
def saturateRGB(color, saturateAmount):
    return (min(255, max(0, color[0] * saturateAmount)), min(255, max(0, color[1] * saturateAmount)), min(255, max(0, color[2] * saturateAmount)))

with open("levels.json") as f:
    levels = json.load(f)["levels"]
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.font.init()
font = pygame.font.SysFont("Calibri", 60,bold=1)
font2 = pygame.font.SysFont("Calibri", 40,bold=1)
level_finished = font.render("Level finished!", True, (0,0,0))

next_button = font.render("NEXT", True, (33, 255, 151), saturateRGB((33, 255, 151), 0.5))
next_button_saturated = font.render("NEXT", True, saturateRGB((33, 255, 151), 1.2), saturateRGB((33, 255, 151), 0.5*1.2))
next_button_size = next_button.get_size()

again_button = font.render("AGAIN", True, (255, 172, 48), saturateRGB((255, 172, 48), 0.5))
again_button_saturated = font.render("AGAIN", True, saturateRGB((255, 172, 48), 1.2), saturateRGB((255, 172, 48), 0.5*1.2))
again_button_size = again_button.get_size()

def minimum_not_negative(a,b):
    if a < 0:
        return b
    if b < 0:
        return a
    return min(a,b)

def get_block_list_to_show(level):
    block_list_to_show = []
    for block in level["blocks"]:
        for b in blocks.blockList:
            if b.prefix == block:
                block_list_to_show.append(b)
                break
    return block_list_to_show

renderers = {"grid":grid_renderer.grid_renderer}

def play_level(index):
    level = levels[index]
    if os.path.isfile(f"player_data/{index}"):
        with open(f"player_data/{index}", "rb") as f:
            player_data = pickle.load(f)
            error_string = f"There was an error loading player data for level {index+1}. \n To fix this, please close the game and delete the file player_data/{index}"
            assert "program" in player_data, error_string
            assert "high_score_size" in player_data, error_string
            assert "high_score_speed" in player_data, error_string
            assert "jump_generator" in player_data, error_string
            assert type(player_data["high_score_size"]) == int, error_string
            assert type(player_data["high_score_speed"]) == int, error_string
            assert type(player_data["program"]) == list, error_string
            for block in player_data["program"]:
                assert hasattr(block, "validateValues"), error_string
                assert block.validateValues(), error_string
    else:
        player_data = {"program":[],"high_score_size":-1,"high_score_speed":-1,"jump_generator":jumpIdGenerator()}
    size = -1
    speed = -1
    program = player_data["program"]
    high_score_size = player_data["high_score_size"]
    high_score_speed = player_data["high_score_speed"]


    challenge_size = level["challenge_size"]
    challenge_speed = level["challenge_speed"]
    size_challenge_succeed = font2.render(f"Size Challenge: {challenge_size}", True, (0, 64, 5))
    speed_challenge_succeed = font2.render(f"Speed Challenge: {challenge_speed}", True, (0, 64, 5))
    size_challenge_fail = font2.render(f"Size Challenge: {challenge_size}", True, (64, 2, 0))
    speed_challenge_fail = font2.render(f"Speed Challenge: {challenge_speed}", True, (64, 2, 0))

    renderer = renderers[level["type"]](screen, blocks.blockList, get_block_list_to_show(level),player_data["jump_generator"], data=level["data"],top_text = level.get("top_text",""))
    renderer.program = program
    try_again = True
    running = True
    while try_again and running:
        running = True
        won = False
        renderer.running = False
        renderer.won = False
        renderer.init_runner(**renderer.runner_init_kwargs)
        while running and not won:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            screen.fill((0,0,0))
            program, won = renderer.tick(events)
            pygame.display.flip()
        if won:
            size = sum(map(lambda x: x.size,program))
            speed = renderer.ticks_passed
            surface = pygame.display.get_surface()
            finished = False
            while running and not finished:
                        
                screen.blit(surface, (0,0))
                w,h = (600,1000)
                x,y = screen.get_width()//2-w//2,screen.get_height()//2-h//2
                again_button_pos = (x+20,y+h-next_button_size[1]-20)
                next_button_pos = (x+w-next_button_size[0]-20,y+h-next_button_size[1]-20)
                again_button_rect = pygame.Rect(*again_button_pos, *again_button_size)
                next_button_rect = pygame.Rect(*next_button_pos, *next_button_size)
                mouse_pos = pygame.mouse.get_pos()
                again_button_hover = again_button_rect.collidepoint(mouse_pos)
                next_button_hover = next_button_rect.collidepoint(mouse_pos)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if again_button_rect.collidepoint(mouse_pos):
                                finished = True
                            elif next_button_rect.collidepoint(mouse_pos):
                                finished = True
                                try_again = False

                pygame.draw.rect(screen, (200,200,200), (x,y,w,h))
                screen.blit(level_finished, (x,y))
                if size <= challenge_size:
                    screen.blit(size_challenge_succeed, (x,y+100))
                    your_size=font2.render(f"Your program's size: {size}", True, (0, 64, 5))
                    screen.blit(your_size, (x,y+150))
                else:
                    screen.blit(size_challenge_fail, (x,y+100))
                    your_size=font2.render(f"Your program's size: {size}", True, (64,2,0))
                    screen.blit(your_size, (x,y+150))
                if high_score_size > -1:
                    hs_size=font2.render(f"previous smallest: {high_score_size}", True, (0,0,0))
                    screen.blit(hs_size, (x,y+200))

                if speed <= challenge_speed:
                    screen.blit(speed_challenge_succeed, (x,y+400))
                    your_speed=font2.render(f"Your program's speed: {speed}", True, (0, 64, 5))
                    screen.blit(your_speed, (x,y+450))
                else:
                    screen.blit(speed_challenge_fail, (x,y+400))
                    your_speed=font2.render(f"Your program's speed: {speed}", True, (64,2,0))
                    screen.blit(your_speed, (x,y+450))
                if high_score_speed > -1:
                    hs_speed=font2.render(f"previous fastest: {high_score_speed}", True, (0,0,0))
                    screen.blit(hs_speed, (x,y+500))
                if again_button_hover:
                    screen.blit(again_button_saturated, again_button_pos)
                else:
                    screen.blit(again_button, again_button_pos)
                if next_button_hover:
                    screen.blit(next_button_saturated, next_button_pos)
                else:
                    screen.blit(next_button, next_button_pos)
                pygame.display.flip()
        with open(f"player_data/{index}", "wb") as f:
            high_score_size = minimum_not_negative(high_score_size, size)
            high_score_speed = minimum_not_negative(high_score_speed, speed)
            pickle.dump({"program":program,"high_score_size":high_score_size,"high_score_speed":high_score_speed,"jump_generator":renderer.jumpIdGenerator}, f)
    return running, won