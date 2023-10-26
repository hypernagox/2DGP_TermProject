
class CScene:
    def __init__(self):
        self.objs = [[] for _ in range(10)]
    def AddObject(self,depth,obj):
        self.objs[depth].append(obj)
    def update(self):
        for arr in self.objs:
            for obj in arr:
                obj.update()
    def late_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.update()
    def last_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.update()
    def final_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.update()
    def render(self):
        for arr in self.objs:
            for obj in arr:
                obj.render()