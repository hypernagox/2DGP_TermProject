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
        self.m_pos = self.m_posOffset
        self.m_posOffset = Vec2()