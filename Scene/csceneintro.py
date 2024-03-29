from Scene.cscene import CScene


class Intro_Scene(CScene):
    def __init__(self,scene_name):
        super().__init__(scene_name)
        from Singletons.resourcemgr import CResMgr
        self.loading_img = CResMgr().GetTex('load.png')
    def update(self):

        from Singletons.ckeymgr import GetKey
        if 'TAP' == GetKey(1):
            from Singletons.eventmgr import ChangeScene
            ChangeScene(self.scene_name,'Stage')
    def render(self):
        self.loading_img.draw_to_origin(
            0,
            0,
            1400,
            700
        )
        from pico2d import load_font
        self.font = load_font('ENCR10B.TTF', 50)
        self.font.draw(700,350,"PRESS LEFT BUTTON",(255,0,0))