from Objects.cobjects import CObject
from Singletons.collisionmgr import resolve_collision


class CBlock(CObject):
    def __init__(self,x,y,size,texture_name):
        super().__init__()
        from vector2 import Vec2
        self.GetTransform().m_pos = Vec2(x,y)
        self.GetTransform().m_size = size
        from Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self)).m_vSizeOffset = Vec2(0,0)
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer(texture_name))

    def OnCollisionEnter(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        if other.group_name == 'PROJ':
            from Singletons.eventmgr import CreateObj
            from Objects.item import CItem
            from vector2 import Vec2
            item = CItem(Vec2(30, 30), self.GetTransform().m_pos, "ball21x21.png")
            CreateObj("ITEM", item)
            item.GetComp("RigidBody").bGravity = True
            from Singletons.eventmgr import DestroyObj

            item2 = CItem(Vec2(30, 30), self.GetTransform().m_pos, "ball21x21.png")
            CreateObj("ITEM", item2)
            item2.GetComp("RigidBody").bGravity = True
            item2.GetComp("RigidBody").SetVelocity(other.dir * - 100)
            item2.GetTransform().m_scale = other.GetTransform().m_scale
            #item2.GetTransform().m_size =
            DestroyObj(self)
        #pene,col_dir = resolve_collision(self,other,True)

    def OnCollisionStay(self,other):
        if None != other.parent and other.group_name == 'ITEM': return
        pene,col_dir = resolve_collision(self, other, True)

    def OnCollisionExit(self,other):
        return
        if other.GetComp("RigidBody"):
            other.GetComp("RigidBody").bIsGround = False

class CGround(CBlock):
    def __init__(self,x,y,size,texture_name):
        super().__init__(x,y,size,texture_name)
        from vector2 import Vec2
        self.GetTransform().m_pos.y = size.y / 2
        #self.GetTransform().m_size.x = 1400



