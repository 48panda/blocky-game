import pygame
import time
import math
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
def angle(A, B, aspectRatio):
    x = B[0] - A[0]
    y = B[1] - A[1]
    angle = math.atan2(-y, x / aspectRatio)
    return angle
def get_point_in_angle(x,y,radius, angle):
    x += radius * math.cos(angle)
    y += -radius * math.sin(angle)
    return (int(x), int(y))
def draw_arrow(screen, pos1, pos2, x3, color = (255,255,255), width = 5):
    x1, y1 = pos1
    x2, y2 = pos2
    x3 = max(x3, max(x1, x2)+30)
    pygame.draw.line(screen, color, (x1, y1), (x3, y1), width)
    pygame.draw.line(screen, color, (x3, y1), (x3, y2), width)
    pygame.draw.line(screen, color, (x3, y2), (x2, y2), width)
    pygame.draw.line(screen, color, (x2, y2), (x2+20, y2+20), width)
    pygame.draw.line(screen, color, (x2, y2), (x2+20, y2-20), width)