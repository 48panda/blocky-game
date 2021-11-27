import win32api, win32con, win32gui
import mouse
import pygame
def move(x,y):
    win32api.SetCursorPos((x,y))
pygame.init()
game = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clear = (12,34,56)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*clear), 0, win32con.LWA_COLORKEY)
running = True
while running:
    game.fill(clear)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display
    pygame.display.update()
