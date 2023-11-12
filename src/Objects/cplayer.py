from sdl2 import SDLK_d, SDLK_a, SDLK_SPACE

from src.Components.animator import CAnimator, CState, CAnimation
from src.Components.camera import CCamera
from src.Components.collider import CCollider
from src.Components.rigidbody import CRigidBody
from src.Components.spriterenderer import CSpriteRenderer
from src.Objects.cobjects import CObject
from src.Singletons.ckeymgr import GetKey
from src.struct.vector2 import Vec2
class CPlayer(CObject):
    def __init__(self):
        super().__init__()
        animator = CAnimator()
        self.AddComponent("Animator",animator)
        walk = StatePlayerWalk()
        walk.anim_torso = CAnimation('Player/walking',0.1,True,0,0,94,98,animator)
        walk.anim_leg = CAnimation('Player/legs', 0.1, True,0,0,94,98,animator)
        animator.AddAnimState('Walk',walk)

        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True,0,0,94,98,animator)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True,0,0,94,98,animator)
        animator.AddAnimState('Idle',idle)
        animator.cur_state = idle

        self.AddComponent("RigidBody",CRigidBody())
        self.AddComponent("SpriteRenderer",CSpriteRenderer())
        cam = CCamera(self)
        cam.SetThisCam2Main()
        self.AddComponent("Camera", cam)
        self.GetTransform().m_size.x = 150
        self.GetTransform().m_size.y = 150
        self.AddComponent("Collider",CCollider(self))
        self.col_count =0
    def update(self):
        super().update()
        rigid = self.GetComp("RigidBody")
        animator = self.GetComp("Animator")
        if 'TAP' == GetKey(SDLK_a):
            rigid.AddVelocity(Vec2(-100,0))
            animator.bIsFlip = True
        if 'HOLD' == GetKey(SDLK_a):
            rigid.AddForce(Vec2(-100,0))
        if 'TAP' == GetKey(SDLK_d):
            rigid.AddVelocity(Vec2(100, 0))
            animator.bIsFlip = False
        if 'HOLD' == GetKey(SDLK_d):
            rigid.AddForce(Vec2(100, 0))
        if 'TAP' == GetKey(SDLK_SPACE):
            rigid.AddVelocity(Vec2(0,100))
            rigid.AddForce(Vec2(0,100))
            rigid.SetIsGround(False)
        from sdl2 import SDLK_r
        if 'HOLD' == GetKey(SDLK_r):
            from src.Singletons.ctimemgr import DT
            self.GetTransform().m_degree += 10 * DT()
    def OnCollisionEnter(self,other):
        print(f'충돌',self.col_count)
        self.col_count += 1
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
