from src.Objects.cobjects import CObject


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
        print('충돌')
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass


