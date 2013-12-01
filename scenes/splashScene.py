'''
Created on 24/05/2009

@author: akathorn
'''

import pygame
from pygame.locals import *
import sceneManager
import time

from scenes import gameScene

class Scene(sceneManager.Scene):
    def __init__(self, sm):
        sceneManager.Scene.__init__(self, sm)
        self.splash1=pygame.image.load("resources/images/splash1.png").convert()
        self.splash2=pygame.image.load("resources/images/splash2.png").convert()
        self.splash=self.splash1
        
        self.alpha=255
        self.alphasurface=pygame.Surface((self.surface.get_width(), self.surface.get_height()))
        self.direction=-1
        self.speed=0.2
        self.lastupdate=0
        self.time=0
        
        
    def update(self, gameTime):
        self.time+=gameTime
        
        if time.time() - self.lastupdate > 0.05:
            self.alpha=self.alpha + self.direction * self.time * self.speed
            if self.alpha > 255:
                self.alpha=255
                self.direction=-1
                if self.splash==self.splash1:
                    self.splash=self.splash2
                    self.speed=0.1
                else:
                    return False
            elif self.alpha < 0:
                self.alpha=0
                self.direction=1
            self.lastupdate=time.time()
            self.time=0
        
        self.surface.blit(self.splash, (0,0))
        
        self.alphasurface.set_alpha(int(self.alpha))
        self.surface.blit(self.alphasurface, (0,0))
        
        self.sm.update_rect(self.surface.get_rect())
        return sceneManager.Scene.update(self, gameTime)
        

    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.sm.sceneList=[]
                return False
            elif evt.type == KEYDOWN:
                return False
            elif evt.type == MOUSEBUTTONDOWN:
                return False
        return True
    