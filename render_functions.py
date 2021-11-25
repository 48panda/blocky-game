import pygame
from vectormath import *
def circle(game,position,radius,color=(255,255,255)):
  position = Vector2(*position)
  size = Vector2(*game.get_size())
  position += Vector2(0.5,0.5)
  position *= size
  position.int()
  pygame.draw.circle(game,color,position,int(size.y*radius))
def line(game,position1,direction,color=(255,255,255),width=1):
  position1 = Vector2(position1)
  position2 = Vector2(direction) + position1
  size = Vector2(game.get_size())
  half = Vector2(0.5,0.5)
  position1 += half
  position2 += half
  position1 *= size
  position2 *= size
  pygame.draw.line(game,color,position1,position2,width)
def box(game,position,size,color=(255,255,255)):
  position = Vector2(position)
  shape = Vector2(size)
  size = Vector2(game.get_size())
  half = Vector2(0.5,0.5)
  position += half
  position *= size
  shape *= size
  pygame.draw.rect(game,color,list(position)+list(shape))
