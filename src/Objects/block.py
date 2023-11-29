from src.Objects.cobjects import CObject
from src.Singletons.collisionmgr import resolve_collision


class CBlock(CObject):
    def __init__(self,x,y,size,texture_name):
        super().__init__()
        from src.struct.vector2 import Vec2
        self.GetTransform().m_pos = Vec2(x,y)
        self.GetTransform().m_size = size
        from src.Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self))
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer(texture_name))

    def OnCollisionEnter(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        resolve_collision(self,other,True)
        #other.GetComp("RigidBody").ResetPhysics()
    def OnCollisionStay(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        resolve_collision(self, other, True)
    def OnCollisionExit(self,other):
        other.GetComp("RigidBody").bIsGround = False

class CGround(CBlock):
    def __init__(self,x,y,size,texture_name):
        super().__init__(x,y,size,texture_name)

