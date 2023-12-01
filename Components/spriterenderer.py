from Components.camera import GetCurMainCam
from Components.camera import CCamera
from Components.component import CComponent

class Sprite:
    def __init__(self):
        self.sprites = None
        self.left = 0
        self.bottom = 0
        self.width = 0
        self.height = 0
class CSpriteRenderer(CComponent):
    def __init__(self,texName = None):
        super().__init__()
        self.bIsCamAffective = True
        from Singletons.resourcemgr import CResMgr
        self.obj_img = None
        if None != texName:
            self.obj_img = CResMgr().GetTex(texName)
        self.deg = 0
    def GetTransformedPos(self):
        trans = self.GetOwner().GetTransform()
        cam = GetCurMainCam()
        self.deg = trans.m_finalDegree
        render_pos = trans.m_finalPos if cam is None or not self.bIsCamAffective else cam.world_to_screen(trans.m_finalPos)
        return (render_pos,trans.m_size,trans.m_finalDegree,trans.m_finalScale)
    def render_target(self,sprite,left,bottom,width,height,bflip):
        render_pos,size,self.deg,scale = self.GetTransformedPos()
        sprite.clip_composite_draw(
            int(left),
            int(bottom),
            int(width),
            int(height),
            int(self.deg),
            '' if not bflip else 'h',
            int(render_pos.x),
            int(render_pos.y),
            int(size.x * scale),
            int(size.y * scale)
        )
    def render(self):
        if None == self.obj_img:
            return
        render_pos,size,self.deg,scale = self.GetTransformedPos()
        self.obj_img.clip_composite_draw(
            int(0),
            int(0),
            int(self.obj_img.w),
            int(self.obj_img.h),
            int(self.deg),
            '',
            int(render_pos.x),
            int(render_pos.y),
            int(size.x *scale),
            int(size.y *scale)
        )