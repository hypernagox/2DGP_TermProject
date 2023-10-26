from singleton import SingletonBase
from pico2d import *

from src.Components.animator import CAnimation
from src.Singletons.ctimemgr import CTimeMgr
from src.Singletons.resourcemgr import CPathMgr,CResMgr


class CCore(metaclass = SingletonBase):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.should_close = False
    def Initialize(self,width,height):
        self.width = width
        self.height = height
        open_canvas(self.width,self.height)
        CPathMgr().Initialize()
        CResMgr().Initialize()
        CTimeMgr().Initialize()
        pass
    def GameLoop(self):
        while not self.should_close:
            update_canvas()
            clear_canvas()
        close_canvas()

CCore().Initialize(800,600)


anim = CAnimation('Monster/wolf/walking',0.2,True)

while True:
    CTimeMgr().update()
    anim.render()
    anim.update()
    update_canvas()
    clear_canvas()