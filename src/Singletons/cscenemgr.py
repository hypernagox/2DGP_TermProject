from singleton import SingletonBase


#from ..Scene.cscene import CScene

class CSceneMgr(metaclass=SingletonBase):
    def __init__(self):
        self.scenes = {}
        self.cur_scene = None
    def AddScene(self,name,scene):
        self.scenes[name] = scene
    def Initialize(self):
        from src.Scene.cscene import CScene
        self.cur_scene = CScene()
        self.scenes['Start']  = self.cur_scene
    def update(self):
        self.cur_scene.update()
        self.cur_scene.late_update()
        self.cur_scene.last_update()
        self.cur_scene.final_update()
    def render(self):
        self.cur_scene.render()
    def GetCurScene(self):
        return self.cur_scene