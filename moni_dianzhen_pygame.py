from dianzhen_font import *
import random
import pygame
SCREEN_WID = 128
SCREEN_HEI = 64
WIN_WID = 640
WIN_HEI = 320
DISPLAY_COLOR = (0, 0, 0)
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

def CreateGround(indexg):
    global ground_load
    buffer = [0x00 for i in range(0, SCREEN_WID)]
    for i in range(0, SCREEN_WID):
        if random.randint(0, 10) > 7:
            randload = random.randint(0, 8)
            for j in range(0, random.randint(1, 6)):
                if i + j >= SCREEN_WID:
                    pass
                else:
                    buffer[i + j] |= 0x01 << randload
    ground_load[indexg] = buffer
def Ground():
    global ground_move
    global ground_state
    ground_move -= 1
    write_gram(ground_move, 5, cactus[0][:9])
    write_gram(ground_move, 6, cactus[0][9:])
    if ground_move > 0:
        write_gram(ground_move, 7, ground_load[0])
        write_gram(ground_move - SCREEN_WID, 7, ground_load[2])
    if ground_move < 0:
        if ground_state == 2:
            CreateGround(1)
            ground_state -= 1
        write_gram(ground_move, 7, ground_load[0])
        write_gram(ground_move + SCREEN_WID, 7, ground_load[1])
    if ground_move < -SCREEN_WID:
        if ground_state == 1:
            CreateGround(2)
            ground_state -= 1
        write_gram(ground_move + SCREEN_WID, 7, ground_load[1])
        write_gram(ground_move + 2 * SCREEN_WID, 7, ground_load[2])
    if ground_move < - (2 * SCREEN_WID):
        ground_move = SCREEN_WID
        ground_state = 2
        CreateGround(0)

def DinoJump():
    pass

def DinoRun():
    global secstate
    if speed % 5 == 0:
        secstate = not secstate
    if secstate:
        write_gram(3, 5, dino[0][:16])
        write_gram(3, 6, dino[0][16:])
    else:
        write_gram(3, 5, dino[1][:16])
        write_gram(3, 6, dino[1][16:])

def MuenView():
    if secstate == 66:
        ShowString(5, 0, 'START')
        ShowString(5, 1, 'LIST')
        ShowString(5, 2, 'QUIT')
    else:
        x = 5
    if secstate == 1:
        ShowString(5, 1, 'LIST')
        ShowString(5, 2, 'QUIT')
        string = 'START'
        y = 0
    elif secstate == 2:
        ShowString(5, 0, 'START')
        ShowString(5, 2, 'QUIT')
        string = 'LIST'
        y = 1
    elif secstate == 3:
        ShowString(5, 0, 'START')
        ShowString(5, 1, 'LIST')
        string = 'QUIT'
        y = 2
    else:
        x = 0
    if x:
        for char in string:
            if x >= SCREEN_WID // 8 :
                x = 0
                y += 1
            up = []
            down = []
            for buffer in ASCIIF8x16[char][:8]:
                up.append(~buffer)
            write_gram(x * 8, y * 2, up)
            for buffer in ASCIIF8x16[char][8:]:
                down.append(~buffer)
            write_gram(x * 8, y * 2 + 1, down)
            x += 1

def ScreenClear():
    clearload = (0 for i in range(0, SCREEN_WID * (SCREEN_HEI // 8)))
    write_gram(0, 0, clearload)

def ShowString(x, y, string):
    if x > SCREEN_WID // 8 or y > SCREEN_HEI // 16:
        print('Out of screen')
        return 0
    for char in string:
        if x >= SCREEN_WID // 8 :
            x = 0
            y += 1
        write_gram(x * 8, y * 2, ASCIIF8x16[char][:8])
        write_gram(x * 8, y * 2 + 1, ASCIIF8x16[char][8:])
        x += 1
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

clock = pygame.time.Clock()
speed = 0





#------------------------------------------start--------------------------------------------#
mainloop = True
while mainloop:
    secstate = 66
    fasstate = 'Muen'
    while fasstate == 'Muen':
        MuenView()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fasstate = 'Quit'
                mainloop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        secstate += 1
                        if secstate > 3:
                            secstate = 1
                if event.button == 3:
                    if secstate == 1:
                        ScreenClear()
                        ground_move = SCREEN_WID
                        ground_load = [[], [], []]
                        CreateGround(0)
                        ground_state = 2
                        write_gram(0, 6, (0x40 for i in range(0, SCREEN_WID)))
                        fasstate = 'Game'
                    if secstate == 2:
                        ScreenClear()
                        ShowString(0, 0, 'waiting...')
                        fasstate = 'List'
                    if secstate == 3:
                        fasstate = 'Quit'
                        mainloop = False
    while fasstate == 'List':
        pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fasstate = 'Quit'
                mainloop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('waiting...')
                if event.button == 3:
                    ScreenClear()
                    fasstate = 'Muen'

    while fasstate == 'Game':
        speed += 1
        Ground()
        DinoRun()
        ShowString(0, 0, str(speed // 10))
        clock.tick(50 + (speed // 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fasstate = 'Quit'
                mainloop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('tiao')
                if event.button == 3:
                    print('pa')
pygame.quit()
