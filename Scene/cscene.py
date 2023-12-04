
GROUP_NAME = {
    "DEFAULT" : 0 ,
    "PLAYER" : 1,
    "MONSTER" : 2,
    "PROJ" : 3,
    "ITEM" : 4,
    "TILE" : 5,
    "GROUND" : 6,
    "FLYING_MONSTER" : 7
}

class CScene:
    def __init__(self):
        self.objs = [[] for _ in range(len(GROUP_NAME))]
        self.layers = [None] * 5
        self.cur_player = None
    def AddObject(self,group_name,obj):
        obj.group_name = group_name
        self.objs[GROUP_NAME[group_name]].append(obj)
    def GetPlayer(self):
        return self.cur_player
    def AddLayer(self,layer,depth = 0):
        self.layers[depth] = layer
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
    def transform_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.components[0].final_update()
    def final_update(self):
        for arr in self.objs:
            for obj in arr:
                obj.final_update()
        for layer in self.layers:
            if layer is None:continue
            layer.update()
    def render(self):
        for layer in self.layers:
            if layer is None: continue
            layer.render()
        for arr in self.objs:
            for obj in arr:
                obj.render()

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
        from vector2 import Vec2
        from Factory.factory import CFactory
        p1 = CFactory.CreateObject('Player')
        self.cur_player = p1
        self.AddObject("PLAYER",p1)
        p2 = CFactory.CreateObject('Monster',Vec2(400, 175),Vec2(100,100),'wolf')
        self.AddObject("MONSTER", p2)

        p3 = CFactory.CreateObject('Monster',Vec2(400, 300),Vec2(100,100) ,'ghost')
        self.AddObject("FLYING_MONSTER", p3)
        p3.SetFlying()
        from Singletons.collisionmgr import RegisterGroup
        RegisterGroup("PLAYER","MONSTER")

        RegisterGroup("PROJ", "MONSTER")
        RegisterGroup("PROJ", "FLYING_MONSTER")

        RegisterGroup("PLAYER","ITEM")

        from vector2 import Vec2

        from Factory.factory import CLayerFactory
        self.AddLayer(CLayerFactory.CreateLayer('sky1.png',
                                                Vec2(0, 0),
                                                Vec2(80, 53),
                                                Vec2(0, 0)), 0)
        self.AddLayer(CLayerFactory.CreateLayer('background.png',
                                                Vec2(0,0),
                                                Vec2(155,100),
                                                Vec2(0,0)),1)
        # self.AddLayer(CLayerFactory.CreateLayer('ground.png',
        #                                         Vec2(0, 0),
        #                                         Vec2(483, 89),
        #                                         Vec2(0, 0),
        #                                         1400 * 2,
        #                                         700 / 4
        #                                         ), 2)
        from Objects.block import CBlock
        def random_position(center, range_x, range_y):
            import random
            random_x = center[0] + random.randint(-range_x, range_x)
            random_y = center[1] + random.randint(-range_y, range_y)
            return Vec2(random_x, random_y)


        center = (1000, 300)
        num_tiles = 100
        range_x, range_y = 1000, 1000
        tile_size = Vec2(100, 100)
        image = 'brick.png'

        for _ in range(num_tiles):

            position = random_position(center, range_x, range_y)


            tile = CBlock(position.x,position.y, tile_size, image)
            self.AddObject("TILE", tile)
        self.AddObject("TILE", CBlock(500,300,Vec2(100,100),'brick.png'))
        RegisterGroup("PLAYER", "TILE")

        from Objects.block import CGround
        for i in range(10):
            self.AddObject("GROUND", CGround(i* 1000, 0, Vec2(1000, 100), 'front.png'))

        RegisterGroup("PLAYER", "GROUND")
        RegisterGroup("MONSTER", "GROUND")
        RegisterGroup("ITEM", "GROUND")

        RegisterGroup("PROJ", "TILE")
        RegisterGroup("ITEM", "TILE")