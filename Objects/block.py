from Objects.cobjects import CObject
from Singletons.collisionmgr import resolve_collision


class CBlock(CObject):
    def __init__(self,x,y,size,texture_name):
        super().__init__()
        from vector2 import Vec2
        self.GetTransform().m_pos = Vec2(x,y)
        self.GetTransform().m_size = size
        from Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self))
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer(texture_name))

    def OnCollisionEnter(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        pene = resolve_collision(self,other,True)
        #other.GetComp("RigidBody").ResetY()
    def OnCollisionStay(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        pene,col_dir = resolve_collision(self, other, True)
        from Singletons.ckeymgr import GetKey
        from sdl2 import SDLK_SPACE
        if col_dir.y == 0 and 'TAP' == GetKey(SDLK_SPACE):
            other.GetComp("RigidBody").AddVelocity(col_dir * 100)
    def OnCollisionExit(self,other):
        other.GetComp("RigidBody").bIsGround = False

class CGround(CBlock):
    def __init__(self,x,y,size,texture_name):
        super().__init__(x,y,size,texture_name)
        from vector2 import Vec2
        self.GetTransform().m_pos.y = size.y / 2
        ##self.GetTransform().m_size = size



