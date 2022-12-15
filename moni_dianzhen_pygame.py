from dianzhen_font import *
import pygame
import time
SCREEN_WID = 128
SCREEN_HEI = 64
WIN_WID = 640
WIN_HEI = 320
DISPLAY_COLOR = (0, 255, 255)
#-------------------------------------------------------------------------------------------#
def write_gram(cursor_x, cursor_y, bytes):
    if cursor_x <= SCREEN_WID and cursor_y <= SCREEN_HEI // 8:
        for a_byte in bytes:
            if cursor_x > 127:
                cursor_x = 0
                cursor_y += 1
            for i in range(0, 8):
                state = a_byte & (0x01 << i)
                show_point(cursor_x, cursor_y * 8 + i, state)
            cursor_x += 1
        pygame.display.flip()
    else:
        print('ERROR ---Cursor out of range')

def show_point(x, y, state):
    dis_x = (x*SingleWidth) + 1
    dis_y = (y*SingleHeight) + 1
    if state:
        pygame.draw.rect(windows, DISPLAY_COLOR, (dis_x, dis_y, SingleWidth-1, SingleHeight-1), 0)
    else:
        pygame.draw.rect(windows, (45,45,45), (dis_x, dis_y, SingleWidth-1, SingleHeight-1), 0)
#-------------------------------------------------------------------------------------------#

def ShowImg():
    pass

def ScreenClear():
    clearload = (0x00 for i in range(0, SCREEN_WID * (SCREEN_HEI // 8)))
    write_gram(0, 0, clearload)

def ShowString(x, y, str):
    if x > SCREEN_WID // 8 or y > SCREEN_HEI // 16:
        print('Out of screen')
        return 0
    for char in str:
        if x >= SCREEN_WID // 8 :
            x = 0
            y += 1
        write_gram(x * 8, y * 2, ASCIIF8x16[char][:8])
        write_gram(x * 8, y * 2 + 1, ASCIIF8x16[char][8:])
        x += 1

def Quit():
    global mainloop
    mainloop = False
    pygame.quit()

#-------------------------------------------init--------------------------------------------#
pygame.init()
windows = pygame.display.set_mode((WIN_WID,WIN_HEI))
windows.fill((45,45,45))
pygame.display.set_caption('moni_dianzhen')

SingleWidth = WIN_WID // SCREEN_WID
SingleHeight = WIN_HEI // SCREEN_HEI
for i in range(0, SCREEN_WID):
    pygame.draw.line(windows, (71,71,71), start_pos=(i*SingleHeight, 0), end_pos=(i*SingleHeight, WIN_HEI), width=1)
for i in range(0, SCREEN_HEI):
    pygame.draw.line(windows, (71,71,71), start_pos=(0, i*SingleWidth), end_pos=(WIN_WID, i*SingleWidth), width=1)
pygame.display.flip()
#------------------------------------------start--------------------------------------------#
mainloop = True
while mainloop:
    write_gram(0, 1, doin[0][:16])
    write_gram(0, 2, doin[0][16:])
    time.sleep(0.1)
    write_gram(0, 1, doin[1][:16])
    write_gram(0, 2, doin[1][16:])
    time.sleep(0.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit()
        if event.type ==pygame.KEYDOWN:
            if event.key == 97:
                ShowString(0, 0, '12')
                ShowString(0, 1, '34')
                time.sleep(0.5)
            elif event.key == 100:
                ScreenClear()
                time.sleep(3)
                Quit()
