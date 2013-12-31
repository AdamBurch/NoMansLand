#! /usr/bin/python

import pygame
from pygame import *
import nml_lib
import nml_platforms

class Player(nml_lib.Entity):
    def __init__(self, x, y):
        nml_lib.Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        
        self.aiming = False
        self.aimAngle = 0
        self.aimPower = 5
        self.powerUpCooldown = nml_lib.CooldownTimer(1)
        self.thrownPlatform = None

    def update(self, up, down, left, right, running, platforms, entities):
        self.aiming = False        
        if down:
            self.aiming = True

        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100

        if self.aiming:
            if up and self.powerUpCooldown.isCooldownUp():
                self.aimPower += 5
                if(self.aimPower > 15):
                    self.aimPower = 5  
                print("aimPower: ", self.aimPower)
                self.powerUpCooldown.burnCooldown()
            if (left or right):
                if right:
                    self.aimAngle -= 5
                if left:
                    self.aimAngle += 5

                if self.aimAngle < 0:
                    self.aimAngle = 0
                if self.aimAngle > 180:
                    self.aimAngle = 180
                print("aimAngle: ", self.aimAngle)
            if running:
                if self.thrownPlatform is None:
                    self.thrownPlatform = nml_platforms.ThrownPlatform(self.rect.left,
                                                         self.rect.top,
                                                         self.aimAngle,
                                                         self.aimPower)
                    entities.add(self.thrownPlatform)

        #TODO EWEWEWEWEWEW
        if self.thrownPlatform is not None:
            self.thrownPlatform.update()
            if not running:
                self.thrownPlatform.burst()
                platforms.append(self.thrownPlatform)
                self.thrownPlatform = None
                
        if not self.aiming:
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if left:
                self.xvel = -8
            if right:
                self.xvel = 8
            if running:
                self.xvel *= 2 
            if not(left or right):
                self.xvel = 0
            
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

            

    #TODO: 
    #   return all the crap I'm colliding with and how
    #   let subclasses decide what to do
    def collide(self, xvel, yvel, platforms):
        returnval = []
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    returnval.append([p, "r"])
                    self.rect.right = p.rect.left
                    print("collide right")
                if xvel < 0:
                    returnval.append([p, "l"])
                    self.rect.left = p.rect.right
                    print ("collide left")
                if yvel > 0:
                    returnval.append([p, "b"])
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    returnval.append([p, "t"])
                    self.rect.top = p.rect.bottom
        return returnval
