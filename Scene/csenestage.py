from Scene.cscene import CScene
from vector2 import Vec2


class Stage_Scene(CScene):
    def __init__(self,scene_name):
        super().__init__(scene_name)
        self.once = False
    def update(self):
        super().update()
        if self.cur_player.GetTransform().m_pos.y >= 4000:
            if self.once: return
            import random
            from Factory.factory import CFactory
            from Singletons.eventmgr import CreateObj

            for i in range(4000, 5000, 50):
                x_position = i + random.randint(0, 100)
                y_position = 5150
                mon = CFactory.CreateObject('Monster', Vec2(x_position, y_position), Vec2(100, 100), 'zombie')
                CreateObj("MONSTER", mon)
                mon.GetTransform().m_pos = Vec2(x_position, y_position)
                mon.GetTransform().m_size = Vec2(200, 200)
                mon.hp = 10
            self.once = True
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
        self.cur_player = p1
        self.AddObject("PLAYER",p1)
        p2 = CFactory.CreateObject('Monster',Vec2(400, 175),Vec2(100,100),'wolf')
        self.AddObject("MONSTER", p2)

        for i in range(200):
           p3 = CFactory.CreateObject('Monster',Vec2(400 + i * 100, 300 + i * 50),Vec2(100,100) ,'ghost')
           self.AddObject("FLYING_MONSTER", p3)
           p3.SetFlying()
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

        def random_position(min_x, max_x, y, existing_positions, tile_size):
            while True:
                import random
                random_x = random.randint(min_x, max_x - tile_size.x)
                new_pos = Vec2(random_x, y)


                overlap = False
                for pos in existing_positions:
                    if (pos.x - tile_size.x < new_pos.x < pos.x + tile_size.x) and \
                            (pos.y - tile_size.y < new_pos.y < pos.y + tile_size.y):
                        overlap = True
                        break

                if not overlap:
                    return new_pos


        num_tiles = 100
        min_x, max_x = 200, 3000
        current_y = 200
        step_y = (3000 - 200) // num_tiles
        tile_size = Vec2(100, 100)
        image = 'brick.png'
        existing_positions = []

        for _ in range(num_tiles):
            position = random_position(min_x, max_x, current_y, existing_positions, tile_size)
            existing_positions.append(position)
            tile = CBlock(position.x, position.y, tile_size, image)
            self.AddObject("TILE", tile)


            current_y += step_y

        RegisterGroup("PLAYER", "TILE")

        from Objects.block import CGround
        for i in range(10):
            self.AddObject("GROUND", CGround(i* 1000, 0, Vec2(1000, 100), 'front.png'))
            self.name = 'main_ground'

        RegisterGroup("PLAYER", "GROUND")
        RegisterGroup("MONSTER", "GROUND")
        RegisterGroup("ITEM", "GROUND")

        RegisterGroup("PROJ", "TILE")
        RegisterGroup("ITEM", "TILE")

        #RegisterGroup("SWORD", "TILE")
        RegisterGroup("SWORD", "MONSTER")
        RegisterGroup("SWORD", "PROJ_MONSTER")

        RegisterGroup("PLAYER", "PORTAL")

        from Objects.portal import CPortal
        portal = CPortal("tree.png")
        self.AddObject("PORTAL",portal)

        bg = CBlock(5000, 5000, Vec2(483 * 10, 11 * 10), 'boss_ground.png')

        bg.name = 'boss_ground'
        self.AddObject("GROUND", bg)

        base_x = 2500


        offset_x = 300

        for i in range(22):
            zigzag_x = base_x + (i % 2) * offset_x
            b = self.AddObject("TILE", CBlock(zigzag_x, 4700 - i * 100, Vec2(100, 120), 'brick2.png'))
            b.name = 'boss_block'

        for i in range(3):
            b = self.AddObject("TILE", CBlock(2400 + i * 100, 2300, Vec2(100, 120), 'brick2.png'))
            b.name = 'boss_block'

    def Exit(self):
        from Singletons.collisionmgr import ResetGroup
        ResetGroup()
        self.cur_player = None
        for obj in self.objs:
            obj.clear()
        self.layers.clear()