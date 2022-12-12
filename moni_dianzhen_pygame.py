import pygame
import time
SCREEN_WID = 128
SCREEN_HEI = 64
WIN_WID = 640
WIN_HEI = 320
DISPLAY_COLOR = (0, 255, 255)

#-------------------------------------------------------------------------------------------#
def show_point(x, y, state):
    dis_x = (x*SingleWidth) + 1
    dis_y = (y*SingleHeight) + 1
    if state:
        pygame.draw.rect(windows, DISPLAY_COLOR, (dis_x, dis_y, SingleWidth-1, SingleHeight-1), 0)
    else:
        pygame.draw.rect(windows, (45,45,45), (dis_x, dis_y, SingleWidth-1, SingleHeight-1), 0)
#-------------------------------------------------------------------------------------------#

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
j = 0
mainloop = True
while mainloop:
    show_point(i, j, True)
    pygame.display.flip()
    show_point(i, j, False)
    time.sleep(0.01)
    i += 1
    if i == SCREEN_WID:
        j += 1
        i = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quit()
