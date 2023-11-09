
GROUP_NAME = {
    "DEFAULT" : 0 ,
    "PLAYER" : 1,
    "MONSTER" : 2,
    "PROJ" : 3
}

class CScene:
    def __init__(self):
        self.objs = [[] for _ in range(10)]
    def AddObject(self,group_name,obj):
        self.objs[GROUP_NAME[group_name]].append(obj)
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
    def Enter(self):
        from src.Factory.factory import CFactory
        p1 = CFactory.CreateObject('Player')
        self.AddObject("PLAYER",p1)