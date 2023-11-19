from src.Singletons.core import CCore


class CLayer:
    def __init__(self,fileName,filelb,filert,worldLeftBottom,width,height):
        from src.Singletons.resourcemgr import CResMgr
        self.layer_img = CResMgr().GetTex(fileName)
        self.left = filelb.x
        self.bottom = filelb.y
        self.right = filert.x
        self.top = filert.y
        from src.Components.spriterenderer import CSpriteRenderer
        self.sprite_renderer = CSpriteRenderer()
        from src.Components.transform import CTransform
        self.transform = CTransform()
        self.transform.m_size.x = width
        self.transform.m_size.y = height
        self.transform.m_pos.x = worldLeftBottom.x + width / 2
        self.transform.m_pos.y = worldLeftBottom.y + height / 2
        self.sprite_renderer.owner = self.transform.owner = self
    def GetTransform(self):
        return self.transform
    def update(self):
        pass
    def render(self):

        screen_width = CCore().width

        from src.Components.camera import GetCurMainCam
        camera_x = GetCurMainCam().m_transform.m_pos.x
        cam_x = (-camera_x) % self.layer_img.w


        self.sprite_renderer.render_target(
            self.layer_img,
            self.left + cam_x - self.layer_img.w,
            self.bottom,
            screen_width,
            self.layer_img.h,
            False
        )


        if cam_x < screen_width:
            self.sprite_renderer.render_target(
                self.layer_img,
                self.left + cam_x,
                self.bottom,
                screen_width - cam_x,
                self.layer_img.h,
                False
            )
