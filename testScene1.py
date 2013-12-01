'''
Created on 24/05/2009

@author: akathorn
'''

import pygame
from pygame.locals import *
import sceneManager
import time

class Scene(sceneManager.Scene):
    def __init__(self, sm):
        sceneManager.Scene.__init__(self, sm)
        self.color=0
        self.direction=1  # 1 or -1
        self.speed=0.1
        self.lastupdate=0
        self.time=0
        
    def update(self, gameTime):
        self.time+=gameTime
        if time.time() - self.lastupdate > 0.05:
            c=int(self.color)
            self.surface.fill((c,c,c))
            self.color=self.color + self.direction * self.time * self.speed
            if self.color > 255:
                self.color=255
                self.direction=-1
            elif self.color < 0:
                self.color=0
                self.direction=1
            self.lastupdate=time.time()
            self.time=0
        
        self.sm.update_rect(self.surface.get_rect())
        return sceneManager.Scene.update(self, gameTime)
        
