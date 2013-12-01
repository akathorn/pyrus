'''
Created on 24/05/2009

@author: akathorn
'''


import pygame
from pygame.locals import *

RENDER_OBJECTS=pygame.sprite.RenderUpdates()
WHITE_CELLS=pygame.sprite.Group()
WHITE_CELLS_R=pygame.sprite.Group()
WHITE_CELLS_G=pygame.sprite.Group()
WHITE_CELLS_B=pygame.sprite.Group()
VIRUS=pygame.sprite.Group()
ANTI=pygame.sprite.Group()

GROUPS=[RENDER_OBJECTS,
        WHITE_CELLS, WHITE_CELLS_R, WHITE_CELLS_G,
        VIRUS, ANTI]

class BaseCell(pygame.sprite.Sprite):
    def __init__(self, tweener, groups=[], pos=(100,100), image="resources/images/blanco_gris.png", intangible=False):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=pos
        
        self.tweener=tweener
        self.tween=None

        self.speed=1   #  pixel/millisecond
        
        self.intangible=intangible
        
    def getPosX(self):
        return self.rect.centerx
        
    def getPosY(self):
        return self.rect.centery
        
    def setPosX(self, pos):
        self.rect.centerx=pos
        
    def setPosY(self, pos):
        self.rect.centery=pos
    
    def update(self, gameTime):
        self.checkCollisions()
       
    def checkCollisions(self):
        pass
        
    
class WhiteCell(BaseCell):
    def moveTo(self, pos):
        if pos[0]==self.getPosX() and pos[1]==self.getPosY():
            return
        if self.tween:
            self.tween.Remove()
        
        changex=pos[0] - self.getPosX()
        changey=pos[1] - self.getPosY()

        dist=(changex ** 2 + changey ** 2) ** 0.5
        
        time=dist * self.speed
        
        self.tween=self.tweener.addTween(self, setPosX=changex, setPosY=changey, tweenTime=time, tweenType=self.tweener.IN_OUT_QUAD)
    
    def checkCollisions(self):
        if self.intangible:
            for obj in pygame.sprite.spritecollide(self, VIRUS, dokill=False, collided=pygame.sprite.collide_circle):
                self.collide(obj)
        for obj in pygame.sprite.spritecollide(self, VIRUS, dokill=False, collided=pygame.sprite.collide_circle):
            WhiteInfectedGreenCell(self.tweener, self.rect.center)
            self.kill()
            

    def collide(self, obj):
        if obj==self: return
        
        diftop=abs(self.rect.top - obj.rect.bottom)
        difbottom=abs(self.rect.bottom - obj.rect.top)
        difright=abs(self.rect.right - obj.rect.left)
        difleft=abs(self.rect.left - obj.rect.right)
        
        
        if difleft > difbottom:
            if difleft > diftop:
                if difleft > difright:
                    obj.speedx*=-1
                    
        if diftop > difbottom:
            if diftop > difright:
                if diftop > difleft:
                    obj.speedy*=-1
                    
        if difright > diftop:
            if difright > difbottom:
                if difright > difleft:
                    obj.speedx*=-1
                    
        if difbottom > diftop:
            if difbottom > difright:
                if difbottom > difleft:
                    obj.speedy*=-1
        
        
    def shoot(self, pos):
        try:
            x=pos[0] - self.rect.centerx
            y=pos[1] - self.rect.centery
            
            h=(x**2 + y**2) ** 0.5
            cos=x/h
            sin=y/h
            
            dir=cos, sin
            
            Anti(pos=self.rect.center, direction=dir)
        except ZeroDivisionError:
            pass
            

class WhiteInfectedGreenCell(BaseCell):
    def __init__(self, tweener, pos):
        BaseCell.__init__(self, tweener, [RENDER_OBJECTS], pos=pos, image="resources/images/blanco_vinfectado.png")
            

class WhiteRedCell(WhiteCell):
    pass

class WhiteGreenCell(WhiteCell):
    pass

class WhiteBlueCell(WhiteCell):
    pass


class Virus(pygame.sprite.Sprite):
    def __init__(self, tweener, groups=[], speed=0.2, direction=(1,1), pos=(100,100), image="resources/images/gvirus.png"):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=pos
        
        self.radius=20
        
        self.tweener=tweener
        self.tween=None

        
        self.speedx=speed * direction[0]   #  pixel/millisecond
        self.speedy=speed * direction[1]   #  pixel/millisecond
        
        self.accumulated_movex=0
        self.accumulated_movey=0
        
    def update(self, gameTime):
        self.move(gameTime)
        self.checkCollisions()
        
    def checkCollisions(self):
        for obj in pygame.sprite.spritecollide(self, VIRUS, dokill=False, collided=pygame.sprite.collide_circle):
            self.collideVirus(obj)
            
        for obj in pygame.sprite.spritecollide(self, ANTI, dokill=True, collided=pygame.sprite.collide_circle):
            self.kill()

    def collideVirus(self, obj):
        if obj==self: return
            
        if obj.rect.top>self.rect.top:
            self.rect.centery-=1
        elif obj.rect.top>self.rect.top:
            self.rect.centery+=1
        else:
            self.rect.centery+=10
            
        if obj.rect.right>self.rect.right:
            self.rect.centerx-=1
        elif obj.rect.right>self.rect.right:
            self.rect.centerx+=1
        else:
            self.rect.centerx+=10
                
        tmpx=obj.speedx
        tmpy=obj.speedy
                
        obj.speedx=self.speedx
        obj.speedy=self.speedy

        self.speedx=tmpx
        self.speedy=tmpy
            
        del tmpx, tmpy


    def move(self, gameTime):
        if self.rect.right + self.speedx > 800:
            self.speedx *= -1
            self.rect.right=799
        if self.rect.left + self.speedx < 0:
            self.speedx *= -1
            self.rect.left=1
        if self.rect.bottom + self.speedy > 600:
            self.speedy *= -1
            self.rect.bottom=599
        if self.rect.top + self.speedy < 0:
            self.speedy *= -1
            self.rect.top=1
        
        
        self.accumulated_movex+=(self.speedx * gameTime)
        self.accumulated_movey+=(self.speedy * gameTime)
        
        self.rect.centerx=self.rect.centerx + int(self.accumulated_movex)
        self.rect.centery=self.rect.centery + int(self.accumulated_movey)
        
        self.accumulated_movex-=int(self.accumulated_movex)
        self.accumulated_movey-=int(self.accumulated_movey)
        
        


class Anti(pygame.sprite.Sprite):
    def __init__(self, groups=[], pos=(100,100), speed=1, direction=(0,1), lifeTime=1, image="resources/images/ganti.png"):
        pygame.sprite.Sprite.__init__(self, [RENDER_OBJECTS, ANTI])
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center=pos
            
        self.speedx=speed * direction[0]   #  pixel/millisecond
        self.speedy=speed * direction[1]   #  pixel/millisecond
        
        self.accumulated_movex=0
        self.accumulated_movey=0
        
        self.life=lifeTime * 1000
        
    def update(self, gameTime):
        self.move(gameTime)

    def move(self, gameTime):
        if self.life < 0:
            self.kill()
        else:
            self.life-=gameTime
        
        if self.rect.right + self.speedx > 800:
            self.speedx *= -1
            self.rect.right=799
        if self.rect.left + self.speedx < 0:
            self.speedx *= -1
            self.rect.left=1
        if self.rect.bottom + self.speedy > 600:
            self.speedy *= -1
            self.rect.bottom=599
        if self.rect.top + self.speedy < 0:
            self.speedy *= -1
            self.rect.top=1
        
        
        self.accumulated_movex+=(self.speedx * gameTime)
        self.accumulated_movey+=(self.speedy * gameTime)
        
        self.rect.centerx=self.rect.centerx + int(self.accumulated_movex)
        self.rect.centery=self.rect.centery + int(self.accumulated_movey)
        
        self.accumulated_movex-=int(self.accumulated_movex)
        self.accumulated_movey-=int(self.accumulated_movey)
        
        
