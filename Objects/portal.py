from Objects.cobjects import CObject


class CPortal(CObject):
    def __init__(self,strTexName):
        super().__init__()
        self.name = "Portal"
        from vector2 import Vec2
        self.GetTransform().m_pos = Vec2(5000, 5150)
        self.GetTransform().m_size = Vec2(200,200)
        from Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))

        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer(strTexName))
        self.delta = 1
    def update(self):
        super().update()
        if self.GetTransform().m_scale >= 3.:
            self.delta = -1
        elif self.GetTransform().m_scale <= 1:
            self.delta = 1
        from Singletons.ctimemgr import DT
        self.GetTransform().m_scale  += 1 * DT() * self.delta

    def OnCollisionEnter(self, other):
        from Singletons.ckeymgr import GetKey
        from sdl2 import SDLK_w
        if 'HOLD' == GetKey(SDLK_w):
            from Singletons.eventmgr import ChangeScene
            from Singletons.cscenemgr import CSceneMgr
            ChangeScene(CSceneMgr().GetCurScene().scene_name, 'Boss')

    def OnCollisionStay(self, other):
        from Singletons.ckeymgr import GetKey
        from sdl2 import SDLK_w
        if 'HOLD' == GetKey(SDLK_w):
            from Singletons.eventmgr import ChangeScene
            from Singletons.cscenemgr import CSceneMgr
            ChangeScene(CSceneMgr().GetCurScene().scene_name, 'Boss')

        pass

    def OnCollisionExit(self, other):
        pass