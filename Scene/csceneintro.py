from Scene.cscene import CScene


class Intro_Scene(CScene):
    def __init__(self):
        super().__init__()

    def update(self):
        from Singletons.ckeymgr import GetKey
        if 'TAP' == GetKey(1):
