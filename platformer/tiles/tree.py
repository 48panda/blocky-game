import os
import sys
import inspect
import pygame
import random
import time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from render_functions import *
from vectormath import *
#All import stuff is above
def rand_float(start,end):
  return start + (random.random() * (end - start)) # utility function
#TODO: group together utility function into utils file

#this whole mess with self.seed is so that the trees don't get re-randomised every frame.
class tree:
  def __init__(self):
    self.seed = random.random()
  def draw(self,game,pos):
    random.seed(self.seed)
    height = -rand_float(0.1,0.2)
    width = rand_float(0.01,0.03)
    box(game,pos,(width,height),color=(164,116,73))
    for i in range(10):
      y = -rand_float(-height-0.04,-height+0.02)
      x = rand_float(-0.01,width+0.01)
      r = rand_float(0.02,0.04)
      c = rand_float(0.2,0.8)
      circle(game,Vector2(x,y)+pos,r,color=(0,255*c,0))
def main():
  game = pygame.display.set_mode((1920//2, 1080//2))
  #game = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  mainLoop = True
  angle = 0
  trees = [tree() for i in range(10)]
  while mainLoop:
      angle += 0
      game.fill((0,0,0))
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              mainLoop = False
      [i.draw(game,(j/11-0.4,0)) for j,i in enumerate(trees)]
      pygame.display.update()

  pygame.quit()
if __name__=="__main__":
  main()
