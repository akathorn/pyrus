# /usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 31/05/2009

@author: akathorn
'''

import pygame
from pygame.locals import *
import sceneManager


class Scene(sceneManager.Scene):
    def __init__(self, sm):
        sceneManager.Scene.__init__(self, sm)
        self.imageList=[
                        "resources/images/help1.png",
                        "resources/images/help2.png"
                        ]
        self.nextImage()
    
    def nextImage(self):
        if not self.imageList: return False
        image=pygame.image.load(self.imageList.pop(0)).convert()
        self.surface.blit(image, (0,0))
        self.sm.update_rect(self.surface.get_rect())
        
        return True
        

    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.sm.sceneList=[]
                return False
            elif evt.type == KEYDOWN:
                if evt.key==pygame.K_ESCAPE:
                    return False
                else:
                    return self.nextImage()
            elif evt.type == MOUSEBUTTONDOWN:
                return self.nextImage()
        return True