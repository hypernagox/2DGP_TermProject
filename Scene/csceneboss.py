from Scene.cscene import CScene


class Boss_Scene(CScene):
    def __init__(self,name):
        super().__init__(name)
        self.scene_name = name

    def Enter(self):
        from vector2 import Vec2

        from ui.cui import CItemUI
        ui = CItemUI(Vec2(50,650),Vec2(50,50),'ball21x21.png')
        self.AddObject("UI", ui)

        import math
        ui2 = CItemUI(Vec2(150, 650), Vec2(100, 50), 'sword.png',90 * (math.pi / 180))
        self.AddObject("UI", ui2)


        from Factory.factory import CFactory
        p1 = CFactory.CreateObject('Player')

        self.AddObject("PLAYER",p1)
        self.cur_player = p1
        from Singletons.collisionmgr import RegisterGroup
        RegisterGroup("PLAYER","MONSTER")

        RegisterGroup("PROJ", "MONSTER")
        RegisterGroup("PROJ", "FLYING_MONSTER")

        RegisterGroup("PLAYER","ITEM")

        from vector2 import Vec2

        from Factory.factory import CLayerFactory
        self.AddLayer(CLayerFactory.CreateLayer('sky2.png',
                                                Vec2(0, 0),
                                                Vec2(80, 53),
                                                Vec2(0, 0)), 0)
        self.AddLayer(CLayerFactory.CreateLayer('background2.png',
                                                Vec2(0,0),
                                                Vec2(155,100),
                                                Vec2(0,0)),1)


        from Objects.block import CGround
        for i in range(2):
            self.AddObject("GROUND", CGround(i* 1000, 0, Vec2(1000, 100), 'front.png'))
            self.name = 'main_ground'

