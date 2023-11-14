
class CLayer:
    def __init__(self,fileName,lb,rt):
        from src.Singletons.resourcemgr import CResMgr
        self.layer_img = CResMgr().GetTex(fileName)
        self.left = lb.x
        self.bottom = lb.y
        self.right = rt.x
        self.top = rt.y
        from src.Components.spriterenderer import CSpriteRenderer
        self.sprite_renderer = CSpriteRenderer()
        from src.Components.transform import CTransform
        self.transform = CTransform()
    def update(self):
        pass

    def render(self):

        pass
