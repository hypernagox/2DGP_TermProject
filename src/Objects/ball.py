from src.Objects.cobjects import CObject


class CBall(CObject):
    def __init__(self,width,height,pos,dir):
        super().__init__()
        self.name = "Ball"
        from src.struct.vector2 import Vec2
        self.GetTransform().m_size = Vec2(width,height)
        self.GetTransform().m_pos = pos
        from src.Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffSet = Vec2(50,50)
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer('ball21x21.png'))
        self.dir = dir.normalized()
    def update(self):
        from src.Singletons.ctimemgr import DT
        self.GetTransform().m_pos += self.dir * 800 * DT()

    def OnCollisionEnter(self,other):
        rigid = other.GetComp("RigidBody")
        rigid.SetVelocity(self.dir * 1000)
        from src.Singletons.eventmgr import DestroyObj
        DestroyObj(self)
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass
