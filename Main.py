import pygame
import random
import win32api
import os
import time
import Load_Files

from pygame import RESIZABLE, MOUSEBUTTONDOWN
from win32con import MOUSEEVENTF_LEFTDOWN

pygame.init()

screen = pygame.display.set_mode((win32api.GetSystemMetrics(0),(win32api.GetSystemMetrics(1))-100),RESIZABLE)
pygame.RESIZABLE = True

background_size = 40
text_font = pygame.font.Font("Romulus.ttf",80)
small_font = pygame.font.Font("Romulus.ttf",50)

text_surf = text_font.render("BLOCK BUILDERS",True,(255,255,255))
mini_text = small_font.render("click to start",True,(255,255,255))

class Block(object):
    def __init__(self,img,size,x_pos,y_pos,function):
        self.fallen = False
        self.block_rect = pygame.image.load(img).convert_alpha()
        self.resized_block = pygame.transform.scale(self.block_rect,(size,size))
        self.function = function
        self.x = x_pos
        self.y = y_pos

        self.rect = pygame.Rect(self.x,self.y,background_size,background_size)

    def run(self):
        self.function()

    def tick(self):
        self.rect = pygame.Rect(round(cube.x/10)*10,round(self.y/10)*10,background_size,background_size+2)


background_image = pygame.image.load("Background.png").convert_alpha()
resized_background = pygame.transform.scale(background_image,(background_size,background_size))

blocks = []

#pygame.time.Clock().tick(60)

pygame.mixer.init()
pygame.mixer.music.load("BlockBox.wav")
pygame.mixer.music.play()

running = True

level_num = 2
startup = True
lvl = Load_Files.load(Load_Files.find_file(level_num))
print(lvl)
transparency = 100
time.sleep(1)
point = (-1,-1)
while running:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    start_fps = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN and not startup:
            blocks.append(
                Block("NORMAL.png", background_size, pygame.mouse.get_pos()[0], 0-background_size, print))
            if (pygame.Rect((0, 0), (64, 64))).collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                point = (-1, -1)
                transparency = 100
                blocks = []
                block_rects = []
                won = 0
        elif event.type == MOUSEBUTTONDOWN:
            startup = False

    for x in range(80):
        for y in range(60):
            screen.blit(resized_background, (x * background_size, y * background_size))
    if not startup:
        screen.blit(pygame.transform.scale(pygame.image.load("Restart.png"),(64,64)),(0,0))



        transparency -= .25
        #block_rects = []
        #for block in blocks:
        #    block_rects.append(block.rect)
        #print(block_rects)


        #for x in range(80):
        #    for y in range(60):
        #        screen.blit(resized_background,(x*background_size,y*background_size))

        won = 0
        for x in range(len(lvl)):
            for y in range(len(lvl)):
                surf = pygame.Surface((background_size,background_size))
                surf.set_alpha(transparency)
                surf.fill((0,0,0))
                screen.blit(surf,(int(lvl[x-1][1]*background_size),round(int((lvl[x-1][0]*background_size)+win32api.GetSystemMetrics(1)-8*background_size-135)/10)*10))
                #print(round((int(lvl[x-1][0]*background_size)+win32api.GetSystemMetrics(1)-8*background_size-150)/10)*10)
                rect = surf.get_rect(topleft = (int(lvl[x-1][1]*background_size)+1,(round(int((lvl[x-1][0]*background_size)+win32api.GetSystemMetrics(1)-8*background_size-135)/10)*10)-1))
                block_rects = [block.rect for block in blocks if block.fallen == 1]
                if rect.collidelist(block_rects) > -1:
                    won += 1/len(lvl)

        print(won)
        if round(won) == len(lvl):
            level_num += 1
            transparency = 100
            blocks = []
            block_rects = []
            won = 0
            lvl = Load_Files.load(Load_Files.find_file(level_num))

        block_rects = []
        for cube in blocks:
            block_rects = [block.rect for block in blocks if not cube is block and block.fallen == True]

            screen.blit(cube.resized_block,(round(cube.x/10)*10,round(cube.y/10)*10))
            pygame.draw.rect(screen,(255,0,0),cube.rect)

            colliding = cube.rect.collidelist(block_rects)
            cube.y += 4 * (cube.y <= win32api.GetSystemMetrics(1)-(100+background_size))
            if colliding != -1:
                cube.y -= 4
                cube.fallen = True
                # print(colliding)
            cube.tick()
            if not cube.y <= win32api.GetSystemMetrics(1)-(100+background_size):
                cube.fallen = True


            #block_rects = [block.rect for block in blocks if not cube is block]

            #print(block_rects)

    else:
        screen.blit(text_surf,((win32api.GetSystemMetrics(0)/2)-(80*6),(win32api.GetSystemMetrics(1)/2)-80))
        screen.blit(mini_text,((win32api.GetSystemMetrics(0)/2)-(80*5),(win32api.GetSystemMetrics(1)/2)))

    pygame.display.flip()
    #print("hi")
    pygame.time.Clock().tick(60)
    time.sleep(.006)
    print(1/(time.time()-start_fps))