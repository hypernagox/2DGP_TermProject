from Scene.cscene import CScene


class Intro_Scene(CScene):
    def __init__(self,scene_name):
        super().__init__(scene_name)

    def update(self):
        from Singletons.ckeymgr import GetKey
        if 'TAP' == GetKey(1):
            from Singletons.eventmgr import ChangeScene
            ChangeScene(self.scene_name,'Stage')
