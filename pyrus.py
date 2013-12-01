# /usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 24/05/2009

@author: akathorn
'''


from sceneManager import *

from scenes import splashScene, gameScene, configScene

while True:
    app=SceneManager(fps=300, debug=False, scene=[splashScene.Scene, configScene.Scene, gameScene.Scene], globito=False)
    r=app.startLoop()
    if r=="repeat":
        continue
    else:
        break