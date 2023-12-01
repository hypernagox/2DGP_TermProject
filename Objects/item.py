from Objects.cobjects import CObject
from vector2 import Vec2


class CItem(CObject):
    def __init__(self,size,pos,item_img_name):
        super().__init__()

        from copy import deepcopy
        self.GetTransform().m_size = deepcopy(size)
        self.GetTransform().m_pos = deepcopy(pos)
        from Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffSet = Vec2(50,50)
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer(item_img_name))
        from Components.rigidbody import CRigidBody
        rigid = self.AddComponent("RigidBody",CRigidBody())
        rigid.SetVelocity(Vec2(0,1) * 100)
        self.ready_to_fire = False
    def update(self):
        super().update()
        if None != self.parent:
            self.GetTransform().OrbitAroundParent(100,2)
            if self.ready_to_fire:
                self.GetTransform().m_size = Vec2(100,100)

    def OnCollisionEnter(self,other):
        if self.parent != None or other.group_name != 'PLAYER':
            return
        from Singletons.cscenemgr import GetCurScene
        self.GetComp("RigidBody").bGravity = False
        GetCurScene().remove_object(self)
        other.AddChild(self)
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass
