from Objects.cobjects import CObject


class CBall(CObject):
    def __init__(self,width,height,pos,dir,scale,life = 3,speed=800):
        super().__init__()
        self.name = "Ball"
        from vector2 import Vec2
        self.GetTransform().m_size = Vec2(width,height)
        self.GetTransform().m_scale = scale
        from copy import deepcopy
        self.GetTransform().m_pos = deepcopy(pos)
        from Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffSet = Vec2(50,50) * scale
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer('ball21x21.png'))
        self.dir = dir.normalized()
        self.acc = 0
        self.life = life
        self.speed = speed
    def update(self):
        from Singletons.ctimemgr import DT
        self.acc += DT()
        self.GetTransform().m_pos += self.dir * self.speed * DT()
        if self.acc >= self.life:
            from Singletons.eventmgr import DestroyObj
            DestroyObj(self)
    def OnCollisionEnter(self,other):
        from Singletons.eventmgr import DestroyObj
        if other.group_name == 'MONSTER' or other.group_name == 'FLYING_MONSTER':
            rigid = other.GetComp("RigidBody")
            rigid.SetVelocity(self.dir * 1000)
            DestroyObj(other)

            DestroyObj(self)
        elif other.group_name == 'TILE':
            DestroyObj(self)
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass
