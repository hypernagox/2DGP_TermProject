from src.Objects.cobjects import CObject


class CItem(CObject):
    def __init__(self,size,pos,item_img_name):
        super().__init__()
        from src.struct.vector2 import Vec2
        self.GetTransform().m_size = size
        self.GetTransform().m_pos = pos
        from src.Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffSet = Vec2(50,50)
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer(item_img_name))
        from src.Components.rigidbody import CRigidBody
        rigid = self.AddComponent("RigidBody",CRigidBody())
        rigid.SetVelocity(Vec2(0,1) * 100)

    def update(self):
        super().update()
        if None != self.parent:
            self.GetTransform().OrbitAroundParent(100,2)
    def OnCollisionEnter(self,other):
        if self.parent != None:
            return
        from src.Singletons.cscenemgr import GetCurScene
        self.GetComp("RigidBody").bGravity = False
        GetCurScene().remove_object(self)
        other.AddChild(self)
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass
