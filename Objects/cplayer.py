from sdl2 import SDLK_d, SDLK_a, SDLK_SPACE, SDLK_r, SDLK_f
from Objects.cobjects import CObject
from Singletons.ckeymgr import GetKey, GetMousePos
from vector2 import Vec2
from Components.animator import CAnimator, CState, CAnimation
class CPlayer(CObject):
    def __init__(self):
        from pico2d import load_font
        self.font = load_font('ENCR10B.TTF', 30)
        self.name = "Player"
        from Components.camera import CCamera
        from Components.collider import CCollider
        from Components.rigidbody import CRigidBody
        from Components.spriterenderer import CSpriteRenderer
        self.hp = 20
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
        attack.anim_atk_sword =  CAnimation('Player/sword', 0.1, False, 0, 0, 94, 98, animator)
        animator.AddAnimState('Attack', attack)
        attack.obj = self
        animator.cur_state = idle

        sp = StatePlayerSpcialAttack()
        sp.anim_atk = CAnimation('Player/punching', 0.01, True, 0, 0, 94, 98, animator)
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

        from Objects.sword import CSword
        self.sword = CSword(self)
        self.AddChild(self.sword)

        self.curWeapon = "BALL"
        from Singletons.cscenemgr import GetUI
        GetUI()[0].bSelect = True

    def update(self):
        super().update()
        #print(self.GetTransform().m_pos.x,self.GetTransform().m_pos.y)
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
        #if 'HOLD' == GetKey(SDLK_r):
        #    from Singletons.ctimemgr import DT
        #    self.GetTransform().m_degree += 10 * DT()
        from sdl2 import SDLK_LEFT
        if self.curWeapon == "BALL":
            if self.curballs and self.player_attack.do_attack(self.curballs[len(self.curballs) - 1]):
                delChild = self.curballs[len(self.curballs) - 1]
                self.curballs.remove(delChild)
                self.EraseChild(delChild)
                delChild.IsDead = True
        from sdl2 import SDLK_1
        from sdl2 import SDLK_2
        if 'TAP' == GetKey(SDLK_1):
            self.curWeapon = "BALL"
            from Singletons.cscenemgr import GetUI
            GetUI()[0].bSelect = True
            GetUI()[1].bSelect = False
        elif 'TAP' == GetKey(SDLK_2):
            self.curWeapon = "SWORD"
            from Singletons.cscenemgr import GetUI
            GetUI()[0].bSelect = False
            GetUI()[1].bSelect = True


        animator.OnSignal()

    def render(self):
        super().render()
        from Components.camera import CCamera
        pos = CCamera.curMainCam.world_to_screen(self.GetTransform().m_pos)
        self.font.draw(int(pos.x - 50),int(pos.y + 100), f'{self.hp}',(255,0,0))
        if self.hp <= 0:
            from Singletons.eventmgr import ChangeScene
            from Singletons.cscenemgr import GetCurScene
            ChangeScene(GetCurScene().scene_name,"Intro")
    def OnCollisionEnter(self,other):
        if other.group_name == "PROJ_MONSTER":
            self.DecreaseHP(1)
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
            if self.obj.player_attack.ball_count >= 20:
                self.obj.player_attack.ball_count -=20
                for _ in range(20):
                    delChild = self.obj.curballs[len(self.obj.curballs) - 1]
                    self.obj.curballs.remove(delChild)
                    self.obj.EraseChild(delChild)
                    delChild.IsDead = True
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
        if 'TAP' == GetKey(SDLK_r):
            if self.obj.player_attack.ball_count >= 20:
                self.obj.player_attack.ball_count -= 20
                for _ in range(20):
                    delChild = self.obj.curballs[len(self.obj.curballs) - 1]
                    self.obj.curballs.remove(delChild)
                    self.obj.EraseChild(delChild)
                    delChild.IsDead = True
                return 'SpecialAttack'
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
        if 'TAP' == GetKey(SDLK_r):
            if self.obj.player_attack.ball_count >= 20:
                self.obj.player_attack.ball_count -= 20
                for _ in range(20):
                    delChild = self.obj.curballs[len(self.obj.curballs) - 1]
                    self.obj.curballs.remove(delChild)
                    self.obj.EraseChild(delChild)
                    delChild.IsDead = True
                return 'SpecialAttack'
        return ''

class StatePlayerAttack(CState):
    def __init__(self):
        self.anim_atk = None
        self.anim_atk_sword = None
        self.is_shoot = True
    def update(self):
        if self.is_shoot:
            self.anim_atk.update()
        else:
            self.anim_atk_sword.update()
    def render(self):
        if self.is_shoot:
            self.anim_atk.render()
        else:
            self.anim_atk_sword.render()
    def enter_state(self):
        self.anim_atk.bFinish = False
        self.anim_atk_sword.bFinish = False
        self.is_shoot = ('BALL' == self.obj.curWeapon)
        if not self.is_shoot:
            self.obj.sword.bActivate = True
    def exit_state(self):
        self.obj.sword.bActivate = False
    def change_state(self):
        if self.is_shoot:
            if self.anim_atk.bFinish:
                return 'Idle'
        else:
            if self.anim_atk_sword.bFinish:
                return 'Idle'
        return ''

def go_fly(obj):
    from Singletons.ctimemgr import DT
    acc = 0
    origin_pos = obj.GetTransform().m_finalPos
    obj.GetComp("RigidBody").bGravity = False
    while True:
        if acc >= 50:
            break
        delta = 1000 * DT()
        obj.GetTransform().m_pos.y += delta
        acc += delta
        yield
    acc = 0
    cnt = 0
    import math
    arc_range = 60
    from Singletons.collisionmgr import RegisterGroup
    RegisterGroup("PROJ", "TILE")
    player_pos = obj.GetObjectScreenPos()
    player_pos_world = obj.GetTransform().m_finalPos
    while True:
        acc += DT()

        mpos = GetMousePos()
        if acc >= 0.01:
            dir_x = mpos.x - player_pos.x
            dir_y = mpos.y - player_pos.y
            base_angle = math.atan2(dir_y, dir_x)
            obj.GetComp("Animator").bFlip = dir_x < 0
            import random
            random_angle = base_angle + math.radians(random.uniform(-arc_range / 2, arc_range / 2))

            direction = Vec2(math.cos(random_angle), math.sin(random_angle))

            from Singletons.eventmgr import CreateObj
            from Objects.ball import CBall
            CreateObj("PROJ", CBall(50, 50,player_pos_world + direction * 10, direction, 1,0.5,2000))
            cnt += 1
            acc = 0

        if cnt >= 50:
            break
        yield
    acc = 0
    go_back = (origin_pos - obj.GetTransform().m_finalPos).normalized()
    while True:
        if acc >= 50:
            break
        delta = 500 * DT()
        obj.GetTransform().m_pos += go_back * delta
        acc += delta
        yield
    RegisterGroup("PROJ", "TILE")


class StatePlayerSpcialAttack(CState):
    def __init__(self):
        self.anim_atk = None

        self.fly_coro = None
    def update(self):
        self.anim_atk.update()
        try:
            next(self.fly_coro)
        except StopIteration:
            self.obj.GetComp("RigidBody").bGravity = True
            self.anim_atk.bRepeat = False
            self.anim_atk.bFinish = True

        #self.anim_atk.bRepeat = False
        #self.anim_atk.bFinish = True
    def render(self):
        self.anim_atk.render()
    def enter_state(self):
        self.anim_atk.bRepeat = True
        self.anim_atk.bFinish = False
        self.fly_coro = go_fly(self.obj)
    def change_state(self):
        if self.anim_atk.bFinish:
            return 'Idle'
        return ''