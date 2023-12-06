import pico2d

from Scene.cscene import CScene


class Dead_Scene(CScene):
    def __init__(self,scene_name):
        super().__init__(scene_name)
        from Singletons.resourcemgr import CResMgr
        self.loading_img2 = CResMgr().GetTex('sky3.png')
        self.loading_img = CResMgr().GetTex('hero.png')
    def update(self):
        from Singletons.ckeymgr import GetKey
        if 'TAP' == GetKey(1):
            from Singletons.eventmgr import ChangeScene
            ChangeScene(self.scene_name,CScene.prev_scene.scene_name)
    def render(self):
        self.loading_img2.draw_to_origin(
            0,
            0,
            1400,
            700
        )
        self.loading_img.draw_to_origin(
            0,
            0,
            1400,
            700
        )
        from pico2d import load_font
        self.font = load_font('ENCR10B.TTF', 100)
        self.font.draw(450,350,"YOU DIED",(255,0,0))
        self.font = load_font('ENCR10B.TTF', 50)
        self.font.draw(300, 250, "Press Left Button To Retry", (255, 0, 0))