from dianzhen_font import ASCIIF8x16
import pygame
import time
SCREEN_WID = 128
SCREEN_HEI = 64
WIN_WID = 640
WIN_HEI = 320
DISPLAY_COLOR = (0, 255, 255)
G_R_A_M = []

#-------------------------------------------------------------------------------------------#
def write_gram(cursor_x, cursor_y, bytes):
    global G_R_A_M
    if cursor_x <= SCREEN_WID and cursor_y <= SCREEN_HEI // 8:
        for a_byte in bytes:
            if cursor_x > 127:
                cursor_x = 0
                cursor_y += 1
            for i in range(0, 8):
                state = a_byte & (0x01 << i)
                show_point(cursor_x, cursor_y * 8 + i, state)
            cursor_x += 1
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

def ShowString(x, y, str):
    if x > SCREEN_WID // 8 or y > SCREEN_HEI // 16:
        print('Out of screen')
        return 0
    for char in str:
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
#------------------------------------------start--------------------------------------------#
i = 0
mainloop = True
while mainloop:
    ShowString(0, 0, 'Hellow World')
    ShowString(0, 3, 't')
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit()
