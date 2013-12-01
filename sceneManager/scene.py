# -*- coding:utf-8 -*-
'''
Created on 24/05/2009

@author: akathorn
'''

import pygame
from pygame.locals import *
import sceneManager

class Scene(object):
    def __init__(self, sm):
        object.__init__(self)
        self.sm=sm
        self.surface=pygame.Surface(sm.screen_size)
        
    def update(self, gameTime):
        if not self.processEvents():
            return False
        else:
            return self.surface 
    
    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                return False
            elif evt.type == KEYDOWN:
                if evt.key==pygame.K_ESCAPE:
                    return False
        return True
    
    
    
    def renderText(self, text, pos=(50,50), color=(0,0,0), font=sceneManager.comicsans, bgcolor=None, marginTop=2, marginSides=2, border=None, borderwidth=2, bg=None):
        try:
            textSprite=font.render(text, 1, color)
        except pygame.error:
            return False

        posx=((pos[0] / 100.0) * self.surface.get_size()[0]) - (textSprite.get_size()[0] / 2.0)
        posy=((pos[1] / 100.0) * self.surface.get_size()[1]) - (textSprite.get_size()[1] / 2.0)
        
        #
        # hacer borderwidth y margin proporcionales al tamaño de la surface
        #
        
        rect=(posx - marginSides,
              posy - marginTop,
              textSprite.get_size()[0] + (marginSides * 2),
              textSprite.get_size()[1] + (marginTop * 2))
        self.sm.update_rect(rect)
        
        if bgcolor:
            pygame.draw.rect(self.surface, bgcolor, rect)
            
        if bg:
            self.surface.blit(self.bg, (posx, posy), rect)
        
        if border:
            pygame.draw.rect(self.surface, border, rect, borderwidth)
        
        self.surface.blit(textSprite, (posx, posy))
        
        return rect
    