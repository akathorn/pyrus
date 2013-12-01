# -*- coding:utf-8 -*-

'''
Created on 30/05/2009

@author: akathorn
'''

from sceneManager import data, basicScenes, fonts
import random

MESSAGES=[
u"Tus defensas han fallado...",
u"Tal vez tendrías que haber tomado más Actimel©",
u"Enhorabuena, eres el orgulloso portador de la Gripe A",
u"El truco es hacer movimientos cortos...",
u"¿Soy el único al que los virus le parecen mocos?",
u"Hay que extirparte la mano derecha, no sabes jugar...",
u"¡Corre! ¡¡¡CORRE!!!... A no espera, ya estás muerto...",
u"Prioriza, ataca a los virus más rápidos",
u"Dispara si no puedes esquivar, esquiva si no puedes disparar",
u"¡Acercate a tus objetivos para apuntar mejor!"
]

#MESSAGES=["a","b"]

random.shuffle(MESSAGES)
msglist=list(MESSAGES)

class Scene(basicScenes.GameOverScene):
    def __init__(self, sm):
        basicScenes.GameOverScene.__init__(self, sm)
        
        global msglist, MESSAGES
        
        if not msglist:
            random.shuffle(MESSAGES)
            msglist=list(MESSAGES)
            
        randommsg=msglist.pop(0)
        
        self.renderText(u"¡Tu célula ha sido infectada!", (50,35), color=(255,255,255), font=fonts.comicsans50)
        self.renderText(randommsg, (50,50), color=(255,255,255), font=fonts.comicsans25)
        
        
        last=data.get().lastScore
        great=data.get().bestScore
        superado=data.get().superado
        
        score=u"Tu puntuación:   %d" % last
        
        if superado:
            msg=u"¡Felicidades, nueva puntuación máxima!"
        elif last == great:
            msg=u"¡Felicidades, has igualado tu puntuación máxima!"
        else:
            msg=u"Tu record de puntuación es %d" % great
            

        
        self.renderText(msg, (50,70), color=(255,255,255), font=fonts.comicsans20)
        self.renderText(score, (50,75), color=(255,255,255))
            