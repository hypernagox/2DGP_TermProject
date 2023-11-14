from src.Objects.cobjects import CObject


class CMonster(CObject):
    def __init__(self):
        super().__init__()
        from src.Components.animator import CAnimator
        animator = CAnimator()
        self.AddComponent("Animator", animator)
        from src.Objects.cplayer import StatePlayerWalk
        walk = StatePlayerWalk()
        from src.Components.animator import CAnimation
        walk.anim_torso = CAnimation('Player/walking', 0.1, True, 0, 0, 94, 98, animator)
        walk.anim_leg = CAnimation('Player/legs', 0.1, True, 0, 0, 94, 98, animator)
        animator.AddAnimState('Walk', walk)
        from src.Objects.cplayer import StatePlayerIdle
        idle = StatePlayerIdle()
        idle.anim_torso = CAnimation('Player/walking', 0.1, True, 0, 0, 94, 98, animator)
        idle.anim_leg = CAnimation('Player/legs', 0.1, True, 0, 0, 94, 98, animator)
        animator.AddAnimState('Idle', idle)
        animator.cur_state = idle
        from src.Components.rigidbody import CRigidBody
        self.AddComponent("RigidBody", CRigidBody())
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer())
        from src.struct.vector2 import Vec2
        self.GetTransform().m_pos = Vec2(300,150)
        self.GetTransform().m_size.x = 100
        self.GetTransform().m_size.y = 100
        from src.Components.collider import CCollider
        self.AddComponent("Collider", CCollider(self))
