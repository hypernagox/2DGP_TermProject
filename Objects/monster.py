from Components.animator import CState
from Objects.cobjects import CObject
class CMonster(CObject):
    def __init__(self,strMonsterName):
        super().__init__()
        self.name = "Monster"
        from Components.animator import CAnimator
        animator = CAnimator()
        self.AddComponent("Animator", animator)
        from Components.animator import CAnimation
        idle = StateMonsterIdle()
        folderName = f'Monster/{strMonsterName}/walking'
        idle.mon_anim = CAnimation(folderName,
                                   0.1,
                                   True,
                                   0,
                                   0,
                                   125,
                                   102
                                   , animator)
        animator.AddAnimState('Idle', idle)
        chase = StateMonsterChase()
        chase.mon_anim = CAnimation(folderName,
                                   0.1,
                                   True,
                                   0,
                                   0,
                                   125,
                                   102
                                   , animator)
        animator.AddAnimState('Chase', chase)
        animator.cur_state = idle
        from Components.rigidbody import CRigidBody
        self.AddComponent("RigidBody", CRigidBody())
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer())
        from vector2 import Vec2
        self.GetTransform().m_pos = Vec2(400, 175)
        self.GetTransform().m_size.x = 100
        self.GetTransform().m_size.y = 100
        from Components.collider import CCollider
        self.AddComponent("Collider", CCollider(self))
    def GetPlayerDirection(self):
        from Singletons.cscenemgr import CSceneMgr
        player = CSceneMgr().GetCurScene().GetPlayer()
        cur_player_pos = player.GetTransform().m_pos
        cur_mon_pos = self.GetTransform().m_pos
        return cur_player_pos - cur_mon_pos
    def OnCollisionEnter(self,other):
        if other.name != "Ball":
            return
        from Singletons.eventmgr import CreateObj
        from Objects.item import CItem
        from vector2 import Vec2
        item = CItem(Vec2(30,30),self.GetTransform().m_finalPos,"ball21x21.png")
        CreateObj("ITEM",item)
        item.GetComp("RigidBody").bGravity=True
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass


class StateMonsterIdle(CState):
    def __init__(self):
        self.mon_anim = None
        self.acc = 0
        self.mon_dir = 1
    def update(self):
        from vector2 import Vec2
        from Singletons.ctimemgr import DT
        self.acc +=  DT() * 100
        if self.acc >= 300:
            self.acc = 0
            self.mon_dir = -self.mon_dir
        self.mon_anim.animator.bIsFlip = True if self.mon_dir == 1 else False
        self.mon_anim.animator.owner.GetTransform().m_pos += Vec2(1,0) * DT() * 100 * self.mon_dir
        self.mon_anim.update()
    def render(self):
        self.mon_anim.render()
    def change_state(self):
        dir = self.mon_anim.animator.owner.GetPlayerDirection()
        if dir.length() <= 300:
            return 'Chase'
        return ''
class StateMonsterChase(CState):
    def __init__(self):
        self.mon_anim = None
        self.angle = 0
    def update(self):
        from Singletons.ctimemgr import DT
        self.mon_anim.animator.owner.GetTransform().m_degree += 10 * DT()
        dir = self.mon_anim.animator.owner.GetPlayerDirection()
        self.mon_anim.animator.bIsFlip = True if dir.x > 0 else False
        dir.normalize()
        self.mon_anim.animator.owner.GetComp("RigidBody").AddVelocity(dir * DT() * 500)
        self.mon_anim.update()
    def render(self):
        self.mon_anim.render()
    def exit_state(self):
        self.mon_anim.animator.owner.GetTransform().m_degree = 0
    def change_state(self):
        dist =  self.mon_anim.animator.owner.GetPlayerDirection()
        if dist.length() >= 400:
            return "Idle"
        return ''