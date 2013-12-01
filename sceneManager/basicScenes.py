'''
Created on 28/05/2009

@author: akathorn
'''

from scene import *
import time
    
class PauseScene(Scene):
    def __init__(self, sm):
        Scene.__init__(self, sm)
        self.bg=pygame.image.load("resources/images/paused.png").convert_alpha()
        self.surface=self.bg.copy()

    def update(self, gameTime):
        pygame.display.update()
        self.sm.update_rect((0,0,self.surface.get_size()[0],self.surface.get_size()[1]))
    
        return Scene.update(self, gameTime)
    
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
        return True
    
    
class GameOverScene(Scene):
    def __init__(self, sm):
        Scene.__init__(self, sm)
        #self.bg=pygame.image.load("resources/images/gameover.png").convert_alpha()
        #self.surface=self.bg.copy()
        
        self.surface.fill((0,0,0))
        
        pygame.display.update()
        self.sm.update_rect((0,0,self.surface.get_size()[0],self.surface.get_size()[1]))
        
        self.start=time.time()
    
    def processEvents(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.sm.close()
                return False
            if time.time() - self.start > 0.4:
                if evt.type == KEYDOWN:
                    return False
                elif evt.type == MOUSEBUTTONDOWN:
                    return False
        return True