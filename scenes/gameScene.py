# -*- coding:utf-8 -*-
'''
Created on 24/05/2009

@author: akathorn
'''

import pygame
from pygame.locals import *
import sceneManager, pyTweener
import time, random
from sceneManager import basicScenes, data
import gameoverScene, pausedScene

Tweener=pyTweener.Tweener()

from cells import *

class Scene(sceneManager.Scene):
    def __init__(self, sm):
        sceneManager.Scene.__init__(self, sm)
        self.bg=pygame.image.load("resources/images/bg.png").convert()
        self.surface=self.bg.copy()
        
        pygame.display.update()
        self.sm.update_rect((0,0,self.surface.get_size()[0],self.surface.get_size()[1]))
        
        self.start()
        
        self.score=0
        
    def start(self):
        level=data.get().level
        self.cell=WhiteCell(Tweener, [RENDER_OBJECTS, WHITE_CELLS], intangible=self.sm.globito)
        
        dif=data.get().difficulty + 1
        numvirus=2 + dif * 4 + 2 * level
        for i in range(0,numvirus+1):
            directionx=random.random() * 2 - 1
            directiony=random.random() * 2 - 1
            direction=directionx, directiony
            pos=(random.randint(200,800), random.randint(200,600))
            speed=0.15 + random.random() * (dif / 30.0)
            Virus(Tweener, groups=(RENDER_OBJECTS, VIRUS), direction=direction, pos=pos, speed=speed)
        
        
        self.timer=0
        self.freezeTime=0
        self.isOver=False
        
        
    def update(self, gameTime):     
        if self.freezeTime>0:
            self.freezeTime -=  gameTime
            return sceneManager.Scene.update(self, gameTime)
        
        if not WHITE_CELLS.sprites() and self.isOver==False:
            self.freezeTime=750
            self.isOver=True
            return sceneManager.Scene.update(self, gameTime)
        elif self.isOver:
            self.gameOver()
            return False
        
        if not VIRUS.sprites():
            self.clean()
            global LEVEL
            data.get().level+=1
            self.start()
        
        Tweener.update(gameTime)
        self.timer+=gameTime
        self.score+=gameTime * (data.get().level + 1) / 1000.0 * (len(VIRUS.sprites()) -1)
        
        WHITE_CELLS.update(gameTime)
        VIRUS.update(gameTime)
        ANTI.update(gameTime)

        
        RENDER_OBJECTS.clear(self.surface, self.bg)
        update_rects=RENDER_OBJECTS.draw(self.surface)
        self.sm.update_rects(update_rects)
        
        infostring=u"Nivel:  %d" % (data.get().level + 1) 
        self.renderText(infostring, (30,98), color=(255,255,255), bg=self.bg)
        
        infostring2=u"Tiempo transcurrido:  %d" % int(self.timer / 1000)
        self.renderText(infostring2, (48,98), color=(255,255,255), bg=self.bg)
        
        infostring3=u"Puntuación:  %d" % int(self.score)
        self.renderText(infostring3, (70,98), color=(255,255,255), bg=self.bg)
        
        
        return sceneManager.Scene.update(self, gameTime)


    def gameOver(self):
        self.clean()
        data.get().newScore(int(self.score))
        data.get().save()
        
        self.sm.sceneList.append(gameoverScene.Scene)
        self.sm.sceneList.append(Scene)
        data.get().level=0

    def clean(self):
        for group in GROUPS:
            group.empty()

    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                return False
            elif evt.type == KEYDOWN:
                if evt.key==pygame.K_ESCAPE:
                    self.sm.pause(pausedScene.Scene)
                elif evt.key==pygame.K_p:
                    self.sm.pause(pausedScene.Scene)
            elif evt.type == MOUSEBUTTONDOWN:
                if evt.button==1:
                    self.cell.moveTo(evt.pos)
                elif evt.button==3:
                    if not len(ANTI.sprites()) > (data.get().difficulty + 1):
                        self.cell.shoot(evt.pos)
        return True
    
    def __del__(self):
        self.clean()
        