from sdl2 import SDLK_d, SDLK_a, SDLK_SPACE
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

        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True,0,0,94,98,animator)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True,0,0,94,98,animator)
        animator.AddAnimState('Idle',idle)

        jump = StatePlayerJump()

        jump.anim_jump = CAnimation('Player/jump', 0.1, True, 0, 0, 94, 98, animator)

        animator.AddAnimState('Jump', jump)

        animator.cur_state = idle

        jump.obj_rigid = self.AddComponent("RigidBody",CRigidBody())
        self.AddComponent("SpriteRenderer",CSpriteRenderer())
        cam = CCamera(self)
        cam.SetThisCam2Main()
        self.GetTransform().m_pos.x = 900
        self.GetTransform().m_pos.y = 175
        self.AddComponent("Camera", cam)
        self.GetTransform().m_size.x = 150
        self.GetTransform().m_size.y = 150
        self.AddComponent("Collider",CCollider(self))
        from Attack.attack import CAttack
        self.player_attack = CAttack(self)
        self.curballs = []


        from Objects.item import CItem
        for _ in range(3):
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
            rigid.AddVelocity(Vec2(0,500))
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
    def change_state(self):
        if 'TAP' == GetKey(SDLK_a) or 'TAP' == GetKey(SDLK_d):
            return 'Walk'
        if 'TAP'== GetKey(SDLK_SPACE):
            return 'Jump'
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
        if 'TAP' == GetKey(SDLK_SPACE):
            return 'Jump'
        return ''

class StatePlayerJump(CState):
    def __init__(self):
        self.anim_jump = None
        self.obj_rigid = None
    def update(self):
        self.anim_jump.update()
    def render(self):
        self.anim_jump.render()
    def change_state(self):
        if self.obj_rigid.bIsGround:
            return 'Idle'
        return ''

class StatePlayerAttack(CState):
    def __init__(self):
        self.anim_atk = None
        self.obj_rigid = None
    def update(self):
        self.anim_atk.update()
    def render(self):
        self.anim_atk.render()
    def change_state(self):
        if self.obj_rigid.bIsGround:
            return 'Idle'
        return ''