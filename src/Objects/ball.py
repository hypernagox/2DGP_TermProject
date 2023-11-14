from src.Objects.cobjects import CObject


class CBall(CObject):
    def __init__(self,width,height,pos,dir):
        super().__init__()
        from src.struct.vector2 import Vec2
        self.GetTransform().m_size = Vec2(width,height)
        self.GetTransform().m_pos = pos
        from src.Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self))
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer('ball21x21.png'))
        self.dir = dir.normalized()
    def update(self):
        from src.Singletons.ctimemgr import DT
        self.GetTransform().m_pos += self.dir * 800 * DT()
