import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
Done = False

def done():
  global Done
  Done = True
  sys.exit()
  exit()
def rg_to_num(r,g,b=0):
  return (360*(r*256+g)/(256*256))-180
def num_to_rg(num):
  num += 180
  num *= 256*256
  num/=360
  return num//256, num % 256
from tkinter import *
from tkinter import filedialog
from PIL import Image
import numpy as np
root = Tk()
root.wm_protocol("WM_DELETE_WINDOW", done)
main_dialog =  Frame(root)
main_dialog.pack()
sliders = []
frames = [[0,0,0,0,0,0,0,0,0,0]]
frame=0
def add_frame():
  global frames
  frames.insert(frame+1,frames[frame].copy())
  next_frame()
for i in range(10):
  sliders+=[[None,None]]
  sliders[i][0]=Scale(main_dialog, from_=0, to=255, orient=HORIZONTAL,showvalue=0)
  sliders[i][0].grid(row=i,column=0)
  sliders[i][0].set(128)
  sliders[i][1]=Scale(main_dialog, from_=0, to=255, orient=HORIZONTAL,showvalue=0)
  sliders[i][1].grid(row=i,column=1)
b = Button(main_dialog,command=add_frame,text="Add frame")
b.grid(row=10,column=0)
def file_save():
    f = filedialog.asksaveasfile(mode='wb', defaultextension=".png")
    if f is None:
        return
    out = []
    for col in frames:
      out+=[[]]
      for pix in col:
        out[-1].append(list(num_to_rg(pix))+[0])
    print(out)
    im = Image.fromarray(np.asarray(out).astype(np.uint8))
    im.save(f)
def file_load():
    f = filedialog.askopenfilename(defaultextension=".png")
    if f is None:
        return
    pic_array = np.array(Image.open(f))
    print(pic_array)
    out = []
    for col in pic_array:
      out+=[[]]
      for pix in col:
        r,g,b = pix
        print(r,g,b)
        out[-1].append(rg_to_num(int(r),int(g)))
    global frames
    frames = out
    set_sliders()
b = Button(main_dialog,command=file_save,text="Save animation")
b.grid(row=11,column=0)
b = Button(main_dialog,command=file_load,text="Load animation")
b.grid(row=11,column=1)
frame_control = Frame(main_dialog)
frame_control.grid(row=10,column=1)
def set_sliders():
  for i in range(10):
    sliders[i][0].set(num_to_rg(frames[frame][i])[0])
    sliders[i][1].set(num_to_rg(frames[frame][i])[1])
def last_frame():
  global frame
  if frame!=0:
    frame-=1
    set_sliders()
    frameText.set(f"Frame {frame+1}")
def next_frame():
  global frame
  if frame!=len(frames)-1:
    frame+=1
    set_sliders()
    frameText.set(f"Frame {frame+1}")
def toggle_play():
  global play
  play = not play
play = False
frameText = StringVar()
frameText.set("Frame 1")
b = Button(frame_control,command=last_frame,text="<")
b.pack(side=LEFT)
b = Button(frame_control,command=toggle_play,text="\u25B6")
b.pack(side=LEFT)
b = Button(frame_control,command=next_frame,text=">")
b.pack(side=LEFT)
l = Label(frame_control,width=9, textvariable=frameText)
l.pack(side=LEFT)
import pygame
import pygame.image
clock = pygame.time.Clock()
background = pygame.image.load("../../assets/background.png")
background = pygame.transform.scale(background,(1920//2, 1080//2))
bg_loc=0
import player_render as player
game = pygame.display.set_mode((1920//2, 1080//2))
#game = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
while not Done:
    clock.tick(10)
    if play:
      frame+=1
      frame%=len(frames)
      set_sliders()
    main_dialog.update()
    game.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done()
    for i,s in enumerate(sliders):
      frames[frame][i] = rg_to_num(s[0].get(),s[1].get())
    game.blit(background,(bg_loc,0))
    game.blit(background,(bg_loc+960,0))
    bg_loc-=10
    if bg_loc==-960:
      bg_loc = 0
    #if frame>0:
    #  player.render(game,(0,0),*frames[frame-1],color=(128,128,128))
    player.render(game,(0,0),*frames[frame])
    #background.scroll(-10,0)
    pygame.display.update()

pygame.quit()
root.destroy()
