from src.Components.component import CComponent
from src.Singletons.core import CCore
from src.struct.vector2 import Vec2


class CCamera(CComponent):
    curMainCam = None
    def __init__(self,obj):
        self.owner = obj
        self.m_transform = obj.GetTransform()
    def world_to_screen(self,world_pos):
        width,height = CCore().GetWidthHeight()
        screen_x = world_pos.x - self.m_transform.m_pos.x + width / 2
        screen_y = world_pos.y - self.m_transform.m_pos.y + height / 2
        return Vec2(screen_x, screen_y)
    def screen_to_world(self,screen_pos):
        width, height = CCore().GetWidthHeight()
        screen_x = screen_pos.x - self.m_transform.m_pos.x + width / 2
        screen_y = screen_pos.y - self.m_transform.m_pos.y + height / 2
        return Vec2(screen_x, screen_y)
    def SetThisCam2Main(self):
        CCamera.curMainCam = self

def GetCurMainCam():
    return CCamera.curMainCam