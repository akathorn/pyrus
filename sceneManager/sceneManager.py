'''
Created on 24/05/2009

@author: akathorn
'''

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
from pygame.locals import *

pygame.init()

from fonts import *

from scene import *
from basicScenes import *
import time
import data

class SceneManager(object):
    def __init__(self, screen_size=(800,600), scene=None, fps=100, debug=True, globito=False, debug_text="Running in debug mode"):
        object.__init__(self)
        
        self.screen_size=screen_size
        
        pygame.display.set_icon(pygame.image.load("resources/images/gvirus.png"))
        if data.get().fullscreen:
            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size)
            
        pygame.display.set_caption("Pyrus")
    
        self.globito=globito
    
        self.fps=fps
        self.debug=debug
        self.debug_text=debug_text
        
        self.clock=pygame.time.Clock()
        self._update_rects=[]
        self.sceneList=[]
        
        self.paused=False
        self.pausedScene=PauseScene(self)
        self.lastsurface=None
        
        if type(scene)==list:
            self.scene=None
            self.sceneList=scene
        elif scene:
            self.scene=scene(self)
        else:
            self.scene=Scene(self)
            
        self.status=0
        
    def pause(self, scene=None):
        if scene: self.pausedScene=scene(self)
        self.paused=True
        
    def unPause(self):
        self.paused=False
        
    def loop(self):
        if not self.scene and not self.sceneList:
            return False
        elif not self.scene and self.sceneList:
            self.nextScene()
        
        if not self.paused:
            sceneSurface=self.updateScene(self.scene)
        elif self.pausedScene:
            sceneSurface=self.updateScene(self.pausedScene)
            if not sceneSurface:
                self.unPause()
                return True
            
        if not sceneSurface:
            if not self.sceneList:
                return False
            else:
                self.nextScene()
                return True
        
        if self.paused:
            self.screen.blit(self.lastsurface, (0,0))
        else:
            self.lastsurface=sceneSurface
            
        self.screen.blit(sceneSurface, (0,0))
            
        if self.debug:
            self.drawDebug()
        
        pygame.display.update(self._update_rects)
        self._update_rects=[]
        
            
        return True

    
    def nextScene(self):
        self.scene=self.sceneList.pop(0)(self)
        
    
    def updateScene(self, scene=None):
        if not scene: scene=self.scene
        self.clock.tick(self.fps)
        gameTime=self.clock.get_time()
            
        sceneSurface=scene.update(gameTime)
            
        return sceneSurface
            
    
    def drawDebug(self):
        debugstring="FPS: %d       %s" % (self.clock.get_fps(), self.debug_text)
        self.renderText(debugstring, (20,1), bg=(255,255,255))
    
    def renderText(self, text, pos=(50,50), color=(0,0,0), font=comicsans, bg=None):
        try:
            textSprite=font.render(text, 1, color)
        except pygame.error:
            return False

        posx=((pos[0] / 100.0) * self.screen.get_size()[0]) - (textSprite.get_size()[0] / 2.0)
        posy=((pos[1] / 100.0) * self.screen.get_size()[1]) - (textSprite.get_size()[1] / 2.0)
        
        self.update_rect((posx,posy,textSprite.get_size()[0],textSprite.get_size()[1]))
        
        if bg:
            rect=pygame.Surface(textSprite.get_size())
            rect.fill(bg)
            self.screen.blit(rect, (posx, posy))
        
        self.screen.blit(textSprite, (posx, posy))
        
        return True
    
    def update_rect(self, rect):
        self._update_rects.append(rect)
    
    def update_rects(self, rects):
        for rect in rects:
         self.update_rect(rect)
        
    def startLoop(self):
        while self.loop():
            pass
        self._close()
        return self.status
        
    def close(self):
        self.sceneList=[]
        self.scene=None
        
    def _close(self):
        data.get().save()
        
        