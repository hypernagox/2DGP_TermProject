from Objects.cobjects import CObject


class CPortal(CObject):
    def __init__(self,strTexName):
        super().__init__()
        self.name = "Portal"
        from vector2 import Vec2
        self.GetTransform().m_pos = Vec2(2600, 2800)
        self.GetTransform().m_size = Vec2(200,200)
        from Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))

        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer(strTexName))
