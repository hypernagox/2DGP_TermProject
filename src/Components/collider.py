from src.Components.component import CComponent
from src.struct.vector2 import Vec2


class CCollider(CComponent):
    g_collider_ID = 0
    def __init__(self,obj):
        super().__init__()
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.m_Collider_ID = CCollider.g_collider_ID
        CCollider.g_collider_ID += 1
        self.m_vOffset = Vec2()
        self.m_vSizeOffset = Vec2()

    def OnCollisionEnter(self,other):
        self.owner.OnCollisionEnter(other.owner)
    def OnCollisionStay(self,other):
        self.owner.OnCollisionStay(other.owner)
    def OnCollisionExit(self,other):
        self.owner.OnCollisionExit(other.owner)