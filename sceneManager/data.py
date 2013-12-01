# -*- coding:utf-8 -*-
'''
Created on 30/05/2009

@author: akathorn
'''

import singleton
import cerealizer

Dumper=cerealizer.Dumper()
DictDumper=cerealizer.DictHandler()

dataFile="./gamedata"

class __Data(singleton.Singleton):
    def __init__(self):
        singleton.Singleton.__init__(self)
        self.lastScore=0
        self.bestScore=0
        self.superado=False
        self.fullscreen=False
        self.difficulty=0
        
        self.load()
        
        self.level=0

    def newScore(self, score):
        self.superado=False
        self.lastScore=score
        if score > self.bestScore:
            self.bestScore=score
            self.superado=True
            
    def load(self):
        try:
            df=open(dataFile, "rb")
            DictDumper.collect(self.__dict__, Dumper)
            DictDumper.undump_data(self.__dict__, Dumper, df)
            df.close()
            
        except IOError:
            print u"Archivo de datos no encontrado, generando uno nuevo"
            self.save()
            
        except ValueError:
            print u"Encontrado error leyendo archivo de datos, se continuará la ejecución del programa (posiblemente se generará de nuevo el archivo)"
            self.save()
            
    def save(self):
        df=open(dataFile, "wb")
        DictDumper.collect(self.__dict__, Dumper)
        DictDumper.dump_data(self.__dict__, Dumper, df)
        df.close()
        

get=singleton.__getSingleton(__Data)
