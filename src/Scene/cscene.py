from src.Objects.cplayer import CPlayer


class CScene:
    def __init__(self):
        self.objs = [[] for _ in range(10)]
        self.objs[1].append(CPlayer())
    def AddObject(self,depth,obj):
        self.objs[depth].append(obj)
    def update(self):
        for arr in self.objs:
            for obj in arr:
                obj.update()
    def late_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.late_update()
    def last_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.last_update()
    def final_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.final_update()
    def render(self):
        for arr in self.objs:
            for obj in arr:
                obj.render()