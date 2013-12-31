#! /usr/bin/python

import pygame
import numpy
from pygame import *
import nml_lib

class Platform(nml_lib.Entity):
    def __init__(self, x, y):
        nml_lib.Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ThrownPlatform(nml_lib.Entity):
    def __init__(self, x, y, aimAngle, aimPower):
        nml_lib.Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#77DDDD"))
        self.rect = Rect(x, y, 32, 32)
        aimAngle = aimAngle * numpy.pi/180
        self.xvel = aimPower * numpy.cos(aimAngle)
        self.yvel = -1 * aimPower * numpy.sin(aimAngle)
        self.isBurst = False

    def burst(self):
        self.isBurst = False

    def update(self):
        self.yvel += 0.3
        # max falling speed
        if self.yvel > 100: self.yvel = 100

        if not self.isBurst:
            self.rect.left += self.xvel
            self.rect.top += self.yvel



class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))
