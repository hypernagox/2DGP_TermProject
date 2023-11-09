from src.Components.component import CComponent
from src.struct.vector2 import Vec2


class CCollider(CComponent):
    def __init__(self,obj):
        super().__init__()
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.m_vOffset = Vec2()
        self.m_xSizeOffset, self.m_ySizeOffset = 0,0
