from Components.animator import CState, CAnimation
from Objects.cobjects import CObject
class CMonster(CObject):
    def __init__(self,start_pos,size,strMonsterName):
        super().__init__()
        self.name = strMonsterName
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
        chase.obj = self
        animator.AddAnimState('Chase', chase)
        animator.cur_state = idle
        from Components.rigidbody import CRigidBody
        self.AddComponent("RigidBody", CRigidBody())
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer())

        self.GetTransform().m_pos = start_pos
        self.GetTransform().m_size = size

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
        if other.group_name == "SWORD": return
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
    def SetFlying(self):
        self.GetComp("RigidBody").bGravity=False
        flying_idle = StateFlyingMonsterIdle(self.GetTransform().m_pos)
        flying_idle.obj = self
        animator = self.GetComp("Animator")
        flying_idle.mon_anim = CAnimation(f'Monster/{self.name}/walking',
                                   0.1,
                                   True,
                                   0,
                                   0,
                                   125,
                                   102
                                   , animator)
        animator.state_map["Idle"] = flying_idle
        animator.cur_state = flying_idle

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
            self.mon_anim.animator.state_map["Idle"].center = self.obj.GetTransform().m_pos + Vec2(100,100)
            return "Idle"
        return ''

from vector2 import Vec2
class StateFlyingMonsterIdle(CState):
    def __init__(self,center):
        self.mon_anim = None
        self.acc = 0
        self.mon_dir = 1
        self.center = center
        self.speed = 5
        self.radius = 100
    def update(self):
        import math
        parent_pos = self.center
        self.m_finalPos = self.obj.GetTransform().m_finalPos
        angle = math.atan2(self.m_finalPos.y - parent_pos.y, self.m_finalPos.x - parent_pos.x)
        from Singletons.ctimemgr import DT
        angle += self.speed * DT()
        new_x = (parent_pos.x + self.radius * math.cos(angle)) - self.m_finalPos.x
        new_y = (parent_pos.y + self.radius * math.sin(angle)) - self.m_finalPos.y
        self.obj.GetTransform().m_posOffset.x = new_x
        self.obj.GetTransform().m_posOffset.y = new_y
    def render(self):
        self.mon_anim.render()
    def change_state(self):
        dir = self.mon_anim.animator.owner.GetPlayerDirection()
        if dir.length() <= 300:
            return 'Chase'
        return ''