from Components.component import CComponent

import sys

from vector2 import Vec2

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
        self.m_finalPos =Vec2()
        self.m_finalScale=1
        self.m_finalDegree=0
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
        from vector2 import Vec2
        self.m_posOffset = Vec2()
        if self.parent:
            self.m_finalPos = self.parent.m_finalPos + self.m_pos
            self.m_finalDegree = self.parent.m_finalDegree + self.m_degree
            self.m_finalScale = self.parent.m_finalScale * self.m_scale
        else:
            self.m_finalPos = self.m_pos
            self.m_finalDegree = self.m_degree
            self.m_finalScale = self.m_scale

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
        from copy import deepcopy
        parent_pos = deepcopy(self.parent.GetWorldPos())
        angle = math.atan2(self.m_finalPos.y - parent_pos.y, self.m_finalPos.x - parent_pos.x)
        from Singletons.ctimemgr import DT
        angle += speed * DT()
        new_x = (parent_pos.x + radius * math.cos(angle)) - self.m_finalPos.x
        new_y = (parent_pos.y + radius * math.sin(angle)) - self.m_finalPos.y
        self.m_posOffset.x = new_x
        self.m_posOffset.y = new_y