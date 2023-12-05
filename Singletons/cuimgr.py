
from Singletons.singleton import SingletonBase


class CUIMgr(metaclass=SingletonBase):
    def __init__(self):
      self.uis = []
    def AddUI(self,ui):
        self.uis.append(ui)
        return ui
    def Initialize(self):
       pass
    def update(self):
        for ui in self.uis:
            ui.update()
            ui.late_update()
            ui.last_update()
            ui.final_update()

    def final_update(self):
        self.cur_scene.final_update()
    def render(self):
        self.cur_scene.render()

def GetCurUI():
    return CUIMgr().uis