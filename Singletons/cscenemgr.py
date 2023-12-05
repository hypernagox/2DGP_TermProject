from Singletons.singleton import SingletonBase


class CSceneMgr(metaclass=SingletonBase):
    def __init__(self):
        self.scenes = {}
        self.cur_scene = None
    def AddScene(self,name,scene):
        self.scenes[name] = scene
    def Initialize(self):
        from Scene.csceneintro import Intro_Scene
        from Scene.csenestage import Stage_Scene

        self.scenes['Intro'] = Intro_Scene('Intro')
        self.scenes['Stage']  = Stage_Scene('Stage')
        from Scene.csceneboss import Boss_Scene
        self.scenes['Boss'] = Boss_Scene('Stage')
        self.cur_scene = self.scenes['Intro']

        #self.cur_scene = self.scenes['Boss']
        self.cur_scene.Enter()
    def update(self):
        self.cur_scene.update()
        self.cur_scene.late_update()
        self.cur_scene.last_update()
        #self.cur_scene.transform_update()
    def final_update(self):
        self.cur_scene.final_update()
    def render(self):
        self.cur_scene.render()
    def GetCurScene(self):
        return self.cur_scene

def GetCurSceneObjects():
    return CSceneMgr().GetCurScene().objs

def GetCurScene():
    return CSceneMgr().GetCurScene()

def GetUI():
    return CSceneMgr().GetCurScene().objs[11]