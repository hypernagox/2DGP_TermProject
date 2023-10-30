from src.Components.component import CComponent

class Sprite:
    def __init__(self):
        self.sprites = None
        self.left = 0
        self.bottom = 0
        self.width = 0
        self.height = 0

class CSpriteRenderer(CComponent):
    def __init__(self):
        super().__init__()
    def render_target(self,sprite,left,bottom,width,height,bflip):
        trans = self.GetOwner().GetTransform()
        flag = '' if not bflip else 'h'
        sprite.clip_composite_draw(
            left,
            bottom,
            width ,
            height ,
            trans.m_degree,
            flag,
            trans.m_pos.x,
            trans.m_pos.y,
            trans.m_size.x,
            trans.m_size.y
        )