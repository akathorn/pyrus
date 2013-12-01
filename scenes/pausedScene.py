# /usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 31/05/2009

@author: akathorn
'''

import pygame.font
from pygame.locals import *
from sceneManager import basicScenes
import configScene, gameScene

class Scene(basicScenes.PauseScene):
    def __init__(self, sm):
        basicScenes.PauseScene.__init__(self, sm)
        self.exitRect=pygame.Rect(65,280,315,110)
        self.returnRect=pygame.Rect(435,280,315,110)
        self.mainmenuRect=pygame.Rect(135,430,525,110)
    
    def click(self, pos):
        if self.exitRect.collidepoint(pos):
            self.sm.close()
            return False
        if self.returnRect.collidepoint(pos):
            return False
        if self.mainmenuRect.collidepoint(pos):
            self.sm.sceneList=[configScene.Scene, gameScene.Scene]
            self.sm.nextScene()
            return False
            
        return True
    
    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.sm.close()
                return False
            elif evt.type == KEYDOWN:
                if evt.key==pygame.K_p\
                or evt.key==pygame.K_ESCAPE\
                or evt.key==pygame.K_SPACE:
                    return False
            elif evt.type == MOUSEBUTTONDOWN:
                if evt.button==1:
                    return self.click(evt.pos)
        return True
    