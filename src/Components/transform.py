from src.Components.component import CComponent
from src.struct.vector2 import Vec2
import sys
sys.setrecursionlimit(10000000)

class CTransform(CComponent):
    def __init__(self):
        super().__init__()
        self.parent = None
        self.childs = []
        self.m_pos = Vec2()
        self.m_size = Vec2()
        self.m_degree = 0
        self.m_scale = 1

        self.m_posOffset = Vec2()

    def GetWorldPos(self,acc = Vec2()):
        if self.parent is not None:
            return self.parent.GetWorldPos(self.m_pos + acc)
        else:
            return self.m_pos + acc
    def GetWorldRotation(self,acc = 0):
        if self.parent is not None:
            return self.parent.GetWorldRotation(self.m_degree + acc)
        else:
            return self.m_degree + acc
    def GetWolrdScale(self,acc = 1):
        if self.parent is not None:
            return self.parent.GetWorldScale(self.m_scale * acc)
        else:
            return self.m_scale * acc
    def AddChild(self,transform):
        transform.parent = self
        self.childs.append(transform)
    def final_update(self):
        self.m_pos += self.m_posOffset
        self.m_posOffset = Vec2()
    def GetLeft(self):
        return self.m_pos.x - self.m_size.x/4
    def GetRight(self):
        return self.m_pos.x + self.m_size.x/4
    def GetBottom(self):
        return self.m_pos.y - self.m_size.y/4
    def GetTop(self):
        return self.m_pos.y + self.m_size.y/4
    def OrbitAroundParent(self, radius, speed):
        if self.parent is None:
            return
        import math
        parent_pos = self.parent.GetWorldPos()
        angle = math.atan2(self.m_pos.y - parent_pos.y, self.m_pos.x - parent_pos.x)
        from src.Singletons.ctimemgr import DT
        angle += speed * DT()
        self.m_pos.x = parent_pos.x + radius * math.cos(angle)
        self.m_pos.y = parent_pos.y + radius * math.sin(angle)