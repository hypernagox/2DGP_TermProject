from Components.animator import CState, CAnimation
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

        p2 = CFactory.CreateObject('Monster', Vec2(1200, 175), Vec2(800, 600), 'fat')
        p2.GetComp("Animator").state_map.clear()
        bossidle = StateBossIdle()
        bossidle.obj = p2
        bossidle.mon_anim = CAnimation(f'Monster/fat/walking',
                                   0.1,
                                   True,
                                   0,
                                   0,
                                   125,
                                   102
                                   ,  p2.GetComp("Animator"))
        p2.GetComp("Animator").state_map["Idle"] =bossidle
        p2.GetComp("Animator").cur_state = bossidle
        self.AddObject("MONSTER", p2)
        for i in range(10):
            from Objects.block import CBlock
            self.AddObject("TILE", CBlock(-100,i*100,Vec2(100,100),'brick.png'))

        for i in range(10):
            from Objects.block import CBlock
            self.AddObject("TILE", CBlock(1400,i*100,Vec2(100,100),'brick.png'))

        for i in range(16):
            from Objects.block import CBlock
            self.AddObject("TILE", CBlock(-100 + i * 100, 1000, Vec2(100, 100), 'brick.png'))

        RegisterGroup("PLAYER", "GROUND")
        RegisterGroup("PLAYER", "TILE")
        RegisterGroup("MONSTER", "GROUND")
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


class StateBossIdle(CState):
    def __init__(self):
        self.mon_anim = None
        self.acc = 0
        self.mon_dir = -1
    def update(self):
        from vector2 import Vec2
        from Singletons.ctimemgr import DT
        self.acc +=  DT() * 800
        if self.acc >= 1000:
            self.acc = 0
            self.mon_dir = -self.mon_dir
        self.mon_anim.animator.bIsFlip = True if self.mon_dir == 1 else False

        self.mon_anim.animator.owner.GetTransform().m_pos += Vec2(1,0) * DT() * 800 * self.mon_dir
        self.mon_anim.update()
    def render(self):
        self.mon_anim.render()
    def change_state(self):

        return ''