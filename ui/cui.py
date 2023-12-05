from Objects.cobjects import CObject


class CUI(CObject):
    def __init__(self,pos,size,texName,deg = 0):
        super().__init__()
        from Components.spriterenderer import CSpriteRenderer
        sp = self.AddComponent("SpriteRenderer",CSpriteRenderer(texName))
        sp.bIsCamAffective = False
        self.GetTransform().m_pos = pos
        self.GetTransform().m_size = size
        self.GetTransform().m_degree = deg
        self.bActivate = True
        from Singletons.cscenemgr import CSceneMgr
        self.player = CSceneMgr().GetCurScene().GetPlayer()
    def render(self):
        if not self.bActivate:
            return
        super().render()
class CItemUI(CUI):
    def __init__(self,pos,size,texName,deg = 0):
        super().__init__(pos,size,texName,deg)
        self.bSelect = False
    def update(self):
        if not self.bSelect:
            return
        from Singletons.ctimemgr import DT
        self.GetTransform().m_degree += 10 * DT()

