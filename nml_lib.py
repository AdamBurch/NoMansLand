#! /usr/bin/python

import pygame
import numpy
import time

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class CooldownTimer():
    def __init__(self, cooldownInSeconds):
        self.cooldownInSeconds = cooldownInSeconds
        self.targetTime = -1

    def burnCooldown(self):
        self.targetTime = time.time() + self.cooldownInSeconds

    def isCooldownUp(self):
        return self.targetTime <= time.time()
