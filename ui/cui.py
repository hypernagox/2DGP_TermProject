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
        super().update()
        if not self.bSelect:
            return
        from Singletons.ctimemgr import DT
        self.GetTransform().m_degree += 10 * DT()


class CClickUI(CUI):
    def __init__(self, pos, size, texName, deg=0):
        super().__init__(pos, size, texName, deg)

    def ptInRect(self):
        from Singletons.ckeymgr import GetConvertMousePos
        mpos = GetConvertMousePos()
        mouse_x = mpos.x
        mouse_y = mpos.y
        center_x = self.GetTransform().m_pos.x
        center_y = self.GetTransform().m_pos.y
        width = self.GetTransform().m_size.x
        height = self.GetTransform().m_size.y
        left = center_x - width / 2
        right = center_x + width / 2
        top = center_y + height / 2
        bottom = center_y - height / 2
        return left <= mouse_x <= right and bottom <= mouse_y <= top