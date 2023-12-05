import random

GROUP_NAME = {
    "DEFAULT" : 0 ,
    "PLAYER" : 1,
    "MONSTER" : 2,
    "PROJ" : 3,
    "ITEM" : 4,
    "TILE" : 5,
    "GROUND" : 6,
    "FLYING_MONSTER" : 7,
    "PORTAL" : 8,
    "SWORD" : 9,
    "UI": 10
}

class CScene:
    def __init__(self,scene_name):
        self.objs = [[] for _ in range(len(GROUP_NAME))]
        self.layers = [None] * 5
        self.cur_player = None
        self.scene_name = scene_name
    def AddObject(self,group_name,obj):
        obj.group_name = group_name
        self.objs[GROUP_NAME[group_name]].append(obj)
        return obj
    def GetPlayer(self):
        return self.cur_player
    def AddLayer(self,layer,depth = 0):
        self.layers[depth] = layer

    def update(self):
        for arr in self.objs:
            for obj in arr:
                if obj.IsDead:
                    continue  # IsDead인 객체는 무시하고 다음 객체로 이동
                obj.update()

    def late_update(self):
        for arr in self.objs:
            for obj in arr:
                if obj.IsDead:
                    continue
                obj.late_update()

    def last_update(self):
        for arr in self.objs:
            for obj in arr:
                if obj.IsDead:
                    continue
                obj.last_update()

    def transform_update(self):
        for arr in self.objs:
            for obj in arr:
                if obj.IsDead:
                    continue
                obj.components[0].final_update()

    def final_update(self):
        for arr in self.objs:
            for obj in arr:
                if obj.IsDead:
                    continue
                obj.final_update()
        for layer in self.layers:
            if layer is None:
                continue
            layer.update()
    def render(self):
        for layer in self.layers:
            if layer is None: continue
            layer.render()
        #for arr in self.objs:
        #    for obj in arr:
         #       obj.render()

        for arr in self.objs:
            for i in range(len(arr) - 1, -1, -1):
                if arr[i].IsDead:
                    del arr[i]
                else:
                    arr[i].render()
    def remove_object(self,delObj):
        for arr in self.objs:
            for obj in arr:
                if obj == delObj:
                    del obj
                    return
    def Enter(self):
        pass

    def Exit(self):
        pass

