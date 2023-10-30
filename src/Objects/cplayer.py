from sdl2 import SDLK_d, SDLK_a, SDLK_SPACE

from src.Components.animator import CAnimator, CState, CAnimation
from src.Components.rigidbody import CRigidBody
from src.Objects.cobjects import CObject
from src.Singletons.ckeymgr import GetKey
from src.struct.vector2 import Vec2


class CPlayer(CObject):
    def __init__(self):
        super().__init__()
        animator = CAnimator()
        self.AddComponent("Animator",animator)
        walk = StatePlayerWalk()
        walk.anim_torso = CAnimation('Player/walking',0.1,True,animator)
        walk.anim_leg = CAnimation('Player/legs', 0.1, True,animator)
        animator.AddAnimState('Walk',walk)

        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True,animator)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True,animator)
        animator.AddAnimState('Idle',idle)
        animator.cur_state = idle
        self.AddComponent("RigidBody",CRigidBody())

    def update(self):
        rigid = self.GetComp("RigidBody")
        if 'TAP' == GetKey(SDLK_a):
            rigid.AddVelocity(Vec2(-100,0))
            print(self.GetTransform().m_pos)
        if 'HOLD' == GetKey(SDLK_a):
            rigid.AddForce(Vec2(-100,0))
        if 'TAP' == GetKey(SDLK_d):
            rigid.AddVelocity(Vec2(100, 0))
            print(self.GetTransform().m_pos)
        if 'HOLD' == GetKey(SDLK_d):
            rigid.AddForce(Vec2(100, 0))
        if 'TAP' == GetKey(SDLK_SPACE):
            rigid.AddVelocity(Vec2(0,100))
            rigid.AddForce(Vec2(0,100))
            rigid.bIsGround = False




class StatePlayerIdle(CState):
    def __init__(self):
        self.anim_torso = None
        self.anim_leg = None
    def update(self):
        pass
    def render(self):
        self.anim_torso.render()
        self.anim_leg.render()
    def change_state(self):
        if 'TAP' == GetKey(SDLK_a) or 'TAP' == GetKey(SDLK_d):
            return 'Walk'
        return ''


class StatePlayerWalk(CState):
    def __init__(self):
        self.anim_torso = None
        self.anim_leg = None
    def update(self):
        self.anim_torso.update()
        self.anim_leg.update()
    def render(self):
        self.anim_torso.render()
        self.anim_leg.render()
    def change_state(self):
        if 'AWAY' == GetKey(SDLK_a) or 'AWAY' == GetKey(SDLK_d):
            return 'Idle'
        return ''
