# -*- coding:utf-8 -*-
'''
Created on 30/05/2009

@author: akathorn
'''


import pygame
from pygame.locals import *
import sceneManager
from sceneManager import scene
from sceneManager import data
import helpScene

class Scene(scene.Scene):
    def __init__(self, sm):
        scene.Scene.__init__(self, sm)

        self.bg=pygame.image.load("resources/images/configbg.png").convert_alpha()
        self.surface=self.bg.copy()
        
        self.sm.update_rect((0,0,self.surface.get_size()[0],self.surface.get_size()[1]))
        
    

        self.difficulty=None
        self.play=None
        self.fullscreen=None
        self.clear=None
        self.help=None
        
        self.cleared=False
        
        self.render()


    def render(self):
        self.renderFullscreen()
        self.renderClear()
        self.renderDifficulty()
        self.renderPlay()
        self.renderHelp()
        
    def renderFullscreen(self):
        if data.get().fullscreen:
            fsmsg="Cambiar a ventana"
        else:
            fsmsg="Cambiar a pantalla completa"

        self.fullscreen=pygame.Rect(self.renderText(fsmsg, (50,40), 
                                              color=(0,0,0), 
                                              font=sceneManager.comicsans20, 
                                              bgcolor=(200,200,100), 
                                              marginTop=10, 
                                              marginSides=50, 
                                              border=(0,0,0),
                                              borderwidth=5
                                              )
        )

    def renderClear(self):
        if data.get().bestScore!=0:
            self.clear=pygame.Rect(self.renderText(u"Borrar puntuación máxima", (50,50), 
                                                  color=(0,0,0), 
                                                  font=sceneManager.comicsans20, 
                                                  bgcolor=(120,120,120), 
                                                  marginTop=10, 
                                                  marginSides=50, 
                                                  border=(0,0,0),
                                                  borderwidth=5
                                                  )
            )
        
    def renderDifficulty(self):
        if data.get().difficulty==2:
            dif=u"Difícil"
            col=(200,100,100)
        elif data.get().difficulty==1:
            dif=u"Intermedio"
            col=(250,200,100)
        else:
            dif=u"Fácil"
            col=(50,250,50)
        
        if self.difficulty:
            self.difficulty.inflate_ip(200,20)
            self.surface.blit(self.bg, self.difficulty.topleft, self.difficulty)
            self.sm.update_rect(self.difficulty)
        self.difficulty=pygame.Rect(self.renderText(dif, (50,60), 
                                              color=(0,0,0), 
                                              font=sceneManager.comicsans20, 
                                              bgcolor=col, 
                                              marginTop=10, 
                                              marginSides=50, 
                                              border=(0,0,0),
                                              borderwidth=5
                                              )
        )
    def renderHelp(self):
        self.help=pygame.Rect(self.renderText("Instrucciones", (50,70), 
                                              color=(0,0,0), 
                                              font=sceneManager.comicsans20, 
                                              bgcolor=(100,200,200), 
                                              marginTop=10, 
                                              marginSides=50, 
                                              border=(0,0,0),
                                              borderwidth=5
                                              )
        )
        
    def renderPlay(self):
        self.play=pygame.Rect(self.renderText("Jugar", (50,90), 
                                              color=(0,0,0), 
                                              font=sceneManager.comicsans20, 
                                              bgcolor=(100,100,200), 
                                              marginTop=10, 
                                              marginSides=50, 
                                              border=(0,0,0),
                                              borderwidth=5
                                              )
        )
        

    def click(self, pos):
        if self.play.collidepoint(pos):
            return False
        
        if self.help.collidepoint(pos):
            self.sm.sceneList.insert(0, Scene)
            self.sm.sceneList.insert(0, helpScene.Scene)
            return False
        
        if self.clear and self.clear.collidepoint(pos) and not self.cleared:
            self.clearScore()
            self.clear.inflate_ip(20,20)
            self.surface.blit(self.bg, self.clear.topleft, self.clear)
            self.sm.update_rect(self.clear)
            
            self.cleared=True
            
        if self.difficulty.collidepoint(pos):
            self.toggleDifficulty()
            
        if self.fullscreen.collidepoint(pos):
            self.toggleFullscreen()
            
        return True

    def toggleFullscreen(self):
        if data.get().fullscreen:
            data.get().fullscreen=False
        else:
            data.get().fullscreen=True
        self.sm.status="repeat"
        self.sm.close()

    def toggleDifficulty(self):
        data.get().difficulty+=1
        if data.get().difficulty > 2:
            data.get().difficulty=0
        self.renderDifficulty()

    def clearScore(self):
        data.get().bestScore=0

    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.sm.close()
                return False
            elif evt.type == KEYDOWN:
                if evt.key==pygame.K_ESCAPE:
                    self.sm.close()
                    return False
                elif evt.key==pygame.K_RETURN:
                    return False
                elif evt.key==pygame.K_SPACE:
                    return False
            elif evt.type == MOUSEBUTTONDOWN:
                if evt.button==1:
                    return self.click(evt.pos)
        return True
    