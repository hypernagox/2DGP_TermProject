from Components.component import CComponent
from Singletons.core import CCore
from vector2 import Vec2


class CCamera(CComponent):
    curMainCam = None
    def __init__(self,obj):
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.camOffset = Vec2(0,-200)
    def world_to_screen(self, world_pos):
        width, height = CCore().GetWidthHeight()
        screen_x = world_pos.x - self.m_transform.m_finalPos.x + width / 2
        screen_y = world_pos.y - self.m_transform.m_finalPos.y + height / 2
        camera_x, camera_y = self.m_transform.m_finalPos.x, self.m_transform.m_finalPos.y
        screen_x += self.camOffset.x
        screen_y += self.camOffset.y
        from copy import deepcopy
        return deepcopy(Vec2(screen_x, screen_y))
    def screen_to_world(self,screen_pos):
        width, height = CCore().GetWidthHeight()
        screen_x = screen_pos.x - self.m_transform.m_finalPos.x + width / 2
        screen_y = screen_pos.y - self.m_transform.m_finalPos.y + height / 2
        return Vec2(screen_x, screen_y)
    def GetCamPos(self):
        from copy import deepcopy
        return deepcopy(self.m_transform.m_finalPos + self.camOffset)
    def SetThisCam2Main(self):
        CCamera.curMainCam = self

def GetCurMainCam():
    return CCamera.curMainCam