#! /usr/bin/python

import pygame
import numpy
from pygame import *
import nml_lib
import nml_player
import nml_platforms

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = nml_player.Player(32, 32)
    platforms = []

    x = y = 0
    level = [
        "",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                           ",
        "P                                           ",
        "P                                           ",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = nml_platforms.Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = nml_platforms.ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(nml_camera, total_level_width, total_level_height)
    entities.add(player)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT: return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                running = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms, entities)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if player.aiming:
            drawAimLine(player,
                        camera,
                        player.aimAngle,
                        player.aimPower,
                        screen)

        #pygame.draw.line(screen, (255,   255,   255), camera.apply(player).center, (0, 0), 10)  
        pygame.display.update()

def drawAimLine(player, camera, angle, power, screen):
        xvel = 20 * numpy.cos(angle * numpy.pi /180)
        yvel = -20 * numpy.sin(angle * numpy.pi /180)
        xvel, yvel = camera.apply(player).centerx + xvel, camera.apply(player).centery + yvel
        pygame.draw.line(screen, (127,   127,   127), camera.apply(player).center, (xvel, yvel), 10)    

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def nml_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    return Rect(l, t, w, h)

if __name__ == "__main__":
    main()
