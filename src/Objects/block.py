from src.Objects.cobjects import CObject
from src.Singletons.collisionmgr import resolve_collision


class CBlock(CObject):
    def __init__(self,x,y,size):
        super().__init__()
        from src.struct.vector2 import Vec2
        self.GetTransform().m_pos = Vec2(x,y)
        self.GetTransform().m_size = size
        from src.Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self))
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer("brick.png"))

    def OnCollisionEnter(self,other):
        resolve_collision(self,other,True)
        other.GetComp("RigidBody").ResetPhysics()
    def OnCollisionStay(self,other):
        resolve_collision(self, other, True)
    def OnCollisionExit(self,other):
        pass


