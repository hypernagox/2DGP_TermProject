from singleton import SingletonBase

class CSceneMgr(metaclass=SingletonBase):
    def __init__(self):
        self.scenes = {}
        self.cur_scene = None
    def AddScene(self,name,scene):
        self.scenes[name] = scene
    def update(self):
        self.cur_scene.update()
        self.cur_scene.late_update()
        self.cur_scene.last_update()
        self.cur_scene.final_update()
    def render(self):
        self.cur_scene.render()