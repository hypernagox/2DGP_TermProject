from src.Components.camera import GetCurMainCam
from src.Components.camera import CCamera
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
        self.bIsCamAffective = True
    def render_target(self,sprite,left,bottom,width,height,bflip):
        trans = self.GetOwner().GetTransform()
        cam = GetCurMainCam()
        render_pos = trans.m_pos if cam is None or not self.bIsCamAffective else cam.world_to_screen(trans.m_pos)
        sprite.clip_composite_draw(
            int(left),
            int(bottom),
            int(width),
            int(height),
            int(trans.m_degree),
            '' if not bflip else 'h',
            int(render_pos.x),
            int(render_pos.y),
            int(trans.m_size.x),
            int(trans.m_size.y)
        )