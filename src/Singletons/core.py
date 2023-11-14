from singleton import SingletonBase
from pico2d import *

#from src.Components.animator import CAnimation
from src.Singletons.ckeymgr import CKeyMgr, GetKey
from src.Singletons.collisionmgr import CCollisionMgr
#from src.Singletons.cscenemgr import CSceneMgr
from src.Singletons.ctimemgr import CTimeMgr
from src.Singletons.eventmgr import CEventMgr
from src.Singletons.resourcemgr import CPathMgr,CResMgr

def GetWidthHeight():
    return CCore().GetWidthHeight()
class CCore(metaclass = SingletonBase):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.should_close = False
    def Initialize(self,width,height):
        from src.Singletons.cscenemgr import CSceneMgr
        self.width = width
        self.height = height
        open_canvas(self.width,self.height)
        CPathMgr().Initialize()
        CResMgr().Initialize()
        CSceneMgr().Initialize()
        CKeyMgr().Initialize()
        CTimeMgr().Initialize()
        pass
    def GetWidthHeight(self):
        return self.width,self.height
    def GameLoop(self):
        from src.Singletons.cscenemgr import CSceneMgr
        while not self.should_close:
            CKeyMgr().update()
            CTimeMgr().update()

            if 'TAP' == GetKey(SDLK_ESCAPE):
                self.should_close = True

            CSceneMgr().update()
            CCollisionMgr().update_collision()
            CSceneMgr().final_update()
            CSceneMgr().render()

            CEventMgr().update()
            update_canvas()
            clear_canvas()

        close_canvas()

#CCore().Initialize(800,600)
#CCore().GameLoop()