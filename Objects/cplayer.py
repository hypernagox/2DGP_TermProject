from sdl2 import SDLK_d, SDLK_a, SDLK_SPACE, SDLK_r
from Objects.cobjects import CObject
from Singletons.ckeymgr import GetKey, GetMousePos
from vector2 import Vec2
from Components.animator import CAnimator, CState, CAnimation
class CPlayer(CObject):
    def __init__(self):
        self.name = "Player"
        from Components.camera import CCamera
        from Components.collider import CCollider
        from Components.rigidbody import CRigidBody
        from Components.spriterenderer import CSpriteRenderer
        super().__init__()
        animator = CAnimator()
        self.AddComponent("Animator",animator)
        walk = StatePlayerWalk()
        walk.anim_torso = CAnimation('Player/walking',0.1,True,0,0,94,98,animator)
        walk.anim_leg = CAnimation('Player/legs', 0.1, True,0,0,94,98,animator)
        animator.AddAnimState('Walk',walk)
        walk.anim_wall =  CAnimation('Player/wall', 0.1, True,0,0,94,98,animator)
        walk.obj = self

        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True,0,0,94,98,animator)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True,0,0,94,98,animator)
        animator.AddAnimState('Idle',idle)
        idle.obj =self

        jump = StatePlayerJump()
        jump.obj = self
        jump.anim_jump = CAnimation('Player/jump', 0.1, True, 0, 0, 94, 98, animator)

        animator.AddAnimState('Jump', jump)


        attack = StatePlayerAttack()

        attack.anim_atk = CAnimation('Player/attack', 0.5, False, 0, 0, 94, 98, animator)

        animator.AddAnimState('Attack', attack)

        animator.cur_state = idle

        sp = StatePlayerSpcialAttack()
        sp.anim_atk = CAnimation('Player/attack', 0.1, True, 0, 0, 94, 98, animator)
        animator.AddAnimState('SpecialAttack', sp)
        sp.obj = self

        jump.obj_rigid = self.AddComponent("RigidBody",CRigidBody())
        self.AddComponent("SpriteRenderer",CSpriteRenderer())
        cam = CCamera(self)
        cam.SetThisCam2Main()
        self.GetTransform().m_finalPos.x = self.GetTransform().m_pos.x = 10
        self.GetTransform().m_pos.y = 200
        self.AddComponent("Camera", cam)
        self.GetTransform().m_size.x = 150
        self.GetTransform().m_size.y = 150
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffset = Vec2(-50,-50)
        from Attack.attack import CAttack
        self.player_attack = CAttack(self)
        self.curballs = []


        from Objects.item import CItem
        for _ in range(10):
            ball = CItem(Vec2(50,50),Vec2(20,20),"ball21x21.png")
            self.curballs.append(ball)
            self.AddChild(ball)
    def update(self):
        super().update()
        rigid = self.GetComp("RigidBody")
        animator = self.GetComp("Animator")
        if 'TAP' == GetKey(SDLK_a):
            rigid.AddVelocity(Vec2(-100,0))
            animator.bIsFlip = True
            #animator.OnSignal()
        if 'HOLD' == GetKey(SDLK_a):
            rigid.AddForce(Vec2(-100,0))
        if 'TAP' == GetKey(SDLK_d):
            rigid.AddVelocity(Vec2(100, 0))
            animator.bIsFlip = False
            #animator.OnSignal()
        if 'HOLD' == GetKey(SDLK_d):
            rigid.AddForce(Vec2(100, 0))
            #animator.OnSignal()
        if 'TAP' == GetKey(SDLK_SPACE) and rigid.bIsGround :
            self.GetTransform().m_pos.y += 20
            rigid.AddVelocity(Vec2(0,600))
            rigid.AddForce(Vec2(0,300))
            rigid.SetIsGround(False)
        from sdl2 import SDLK_r
        if 'HOLD' == GetKey(SDLK_r):
            from Singletons.ctimemgr import DT
            self.GetTransform().m_degree += 10 * DT()
        from sdl2 import SDLK_LEFT
        if self.curballs and self.player_attack.do_attack(self.curballs[len(self.curballs) - 1]):
            delChild = self.curballs[len(self.curballs) - 1]
            self.curballs.remove(delChild)
            self.EraseChild(delChild)
            delChild.IsDead = True
        animator.OnSignal()
    def OnCollisionEnter(self,other):
        if None == other.parent and other.group_name == 'ITEM':
            self.curballs.append(other)
            self.player_attack.ball_count += 1
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass


class StatePlayerIdle(CState):
    def __init__(self):
        self.anim_torso = None
        self.anim_leg = None
    def update(self):
        pass
    def render(self):
        self.anim_torso.render()
        self.anim_leg.render()
    def enter_state(self):
        self.obj.GetComp("RigidBody").bIsGround=False
    def change_state(self):
        if 'HOLD' == GetKey(SDLK_a) or 'HOLD' == GetKey(SDLK_d):
            return 'Walk'
        if 'TAP'== GetKey(SDLK_SPACE):
            return 'Jump'
        if 'AWAY' == GetKey(1):
            return "Attack"
        if 'TAP' == GetKey(SDLK_r):
            return 'SpecialAttack'
        return ''


class StatePlayerWalk(CState):
    def __init__(self):
        self.anim_torso = None
        self.anim_leg = None
        self.is_wall = False
        self.anim_wall = None
    def update(self):
        self.is_wall = self.obj.GetComp("RigidBody").bIsGround and self.obj.GetComp("Collider").cur_col_target == "TILE" and abs(self.obj.GetComp("Collider").cur_pene.y) < 0.01

        if not self.is_wall:
            self.anim_torso.update()
            self.anim_leg.update()
        else:
            self.anim_wall.update()
    def render(self):
        if not self.is_wall:
            self.anim_torso.render()
            self.anim_leg.render()
        else:
            self.anim_wall.render()
    def change_state(self):
        if 'AWAY' == GetKey(SDLK_a) or 'AWAY' == GetKey(SDLK_d):
            return 'Idle'
        if 'TAP' == GetKey(SDLK_SPACE):
            return 'Jump'
        if 'AWAY' == GetKey(1):
            return "Attack"
        return ''

class StatePlayerJump(CState):
    def __init__(self):
        self.anim_jump = None
        self.obj_rigid = None
    def update(self):
        self.anim_jump.update()
        from Singletons.ctimemgr import DT
        self.obj.GetTransform().m_degree += 10 * DT()
    def enter_state(self):
        self.anim_jump.bFinish = False
    def exit_state(self):
        self.obj.GetTransform().m_degree = 0
        self.obj_rigid.SetIsGround(False)
    def render(self):
        self.anim_jump.render()
    def change_state(self):
        if self.obj_rigid.bIsGround:
            return 'Idle'
        if 'AWAY' == GetKey(1):
            return "Attack"
        return ''

class StatePlayerAttack(CState):
    def __init__(self):
        self.anim_atk = None
    def update(self):
        self.anim_atk.update()
    def render(self):
        self.anim_atk.render()
    def enter_state(self):
        self.anim_atk.bFinish = False
    def change_state(self):
        if self.anim_atk.bFinish:
            return 'Idle'
        return ''

def go_fly(obj):
    from Singletons.ctimemgr import DT
    acc = 0
    obj.GetComp("RigidBody").bGravity = False
    while True:
        if acc >= 200:
            break
        delta = 10 * DT()
        acc += delta
        obj.GetTransform().m_pos.y += delta
        yield acc


class StatePlayerSpcialAttack(CState):
    def __init__(self):
        self.anim_atk = None
    def update(self):
        self.anim_atk.update()
        for acc in go_fly(self.obj):
            if acc >= 200:
                self.obj.GetComp("RigidBody").bGravity = True
                break
        self.anim_atk.bRepeat = False
        self.anim_atk.bFinish = True
    def render(self):
        self.anim_atk.render()
    def enter_state(self):
        self.anim_atk.bRepeat = True
        self.anim_atk.bFinish = False
    def change_state(self):
        if self.anim_atk.bFinish:
            return 'Idle'
        return ''