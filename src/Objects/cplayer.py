from sdl2 import SDLK_d, SDLK_a

from src.Components.animator import CAnimator, CState, CAnimation
from src.Objects.cobjects import CObject
from src.Singletons.ckeymgr import GetKey


class CPlayer(CObject):
    def __init__(self):
        super().__init__()
        animator = CAnimator()
        self.AddComponent("Animator",animator)
        walk = StatePlayerWalk()
        walk.anim_torso = CAnimation('Player/walking',0.1,True)
        walk.anim_leg = CAnimation('Player/legs', 0.1, True)
        animator.AddAnimState('Walk',walk)

        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True)
        animator.AddAnimState('Idle',idle)
        animator.cur_state = idle


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
