
from pico2d import *

from Singletons.singleton import SingletonBase
from Singletons.resourcemgr import CPathMgr

from Singletons.resourcemgr import CResMgr
from Singletons.cscenemgr import CSceneMgr

from Singletons.ckeymgr import CKeyMgr, GetKey

from Singletons.ctimemgr import CTimeMgr

def GetWidthHeight():
    return CCore().GetWidthHeight()
class CCore(metaclass = SingletonBase):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.should_close = False
    def Initialize(self,width,height):

        self.width = width
        self.height = height
        open_canvas(self.width,self.height)
        from Singletons.resourcemgr import CPathMgr
        CPathMgr().Initialize()
        from Singletons.resourcemgr import CResMgr
        CResMgr().Initialize()
        from Singletons.cscenemgr import CSceneMgr
        CSceneMgr().Initialize()
        from Singletons.ckeymgr import CKeyMgr
        CKeyMgr().Initialize()
        from Singletons.ctimemgr import CTimeMgr
        CTimeMgr().Initialize()
        pass
    def GetWidthHeight(self):
        return self.width,self.height
    def GameLoop(self):
        from Singletons.cscenemgr import CSceneMgr
        while not self.should_close:
            CKeyMgr().update()
            CTimeMgr().update()

            if 'TAP' == GetKey(SDLK_ESCAPE):
                self.should_close = True

            CSceneMgr().update()
            from Singletons.collisionmgr import CCollisionMgr
            CCollisionMgr().update_collision()
            CSceneMgr().final_update()
            CSceneMgr().render()

            from Singletons.eventmgr import CEventMgr
            CEventMgr().update()
            update_canvas()
            clear_canvas()

        close_canvas()

#CCore().Initialize(800,600)
#CCore().GameLoop()