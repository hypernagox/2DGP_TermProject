from Objects.cobjects import CObject


class UI(CObject):
    def __init__(self,pos,size,texName):
        super().__init__()
        from Components.spriterenderer import CSpriteRenderer
        sp = self.AddComponent("SpriteRenderer",CSpriteRenderer('ball21x21.png'))
        sp.bIsCamAffective = False
        self.GetTransform().m_pos = pos
        self.GetTransform().m_size = size

