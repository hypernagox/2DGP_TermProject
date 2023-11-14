from src.Components.animator import CState
from src.Objects.cobjects import CObject
class CMonster(CObject):
    def __init__(self):
        super().__init__()
        from src.Components.animator import CAnimator
        animator = CAnimator()
        self.AddComponent("Animator", animator)
        from src.Components.animator import CAnimation
        idle = StateMonsterIdle()
        idle.mon_anim = CAnimation('Monster/wolf/walking',
                                   0.1,
                                   True,
                                   0,
                                   0,
                                   125,
                                   102
                                   , animator)
        animator.AddAnimState('Idle', idle)
        animator.cur_state = idle
        from src.Components.rigidbody import CRigidBody
        self.AddComponent("RigidBody", CRigidBody())
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer())
        from src.struct.vector2 import Vec2
        self.GetTransform().m_pos = Vec2(300, 175)
        self.GetTransform().m_size.x = 100
        self.GetTransform().m_size.y = 100
        from src.Components.collider import CCollider
        self.AddComponent("Collider", CCollider(self))


class StateMonsterIdle(CState):
    def __init__(self):
        self.mon_anim = None
    def update(self):
        pass
    def render(self):
        self.mon_anim.render()
    def change_state(self):
        return ''