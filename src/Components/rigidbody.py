from src.Components.component import CComponent
from src.Singletons.ctimemgr import DT
from src.struct.vector2 import Vec2


class CRigidBody(CComponent):
    def __init__(self):
        super().__init__()
        self.vForce = Vec2()
        self.vAccel = Vec2()
        self.vVelocity = Vec2()
        self.vMaxVelocity = Vec2(100,500)
        self.fMass = 1
        self.fFriction = 100
        self.bGravity = True
        self.bIsGround = True
        self.bDirty = True
    def SetIsGround(self,b):
        self.bIsGround = b
        if self.bIsGround:
            self.vVelocity.y = 0
        else:
            self.GetOwner().GetTransform().m_pos.y += 1
    def Move(self):
        trans = self.GetOwner().GetTransform()
        trans.m_posOffset += self.vVelocity * DT()
    def update_gravity(self):
        if self.bGravity and not self.bIsGround:
            self.AddForce(Vec2(0,-300))
    def update_physics(self):
        self.vAccel = self.vForce / self.fMass
        self.vVelocity += self.vAccel * DT()
        if not self.vVelocity.is_zero():
            vFriction = self.vVelocity.normalized() * self.fFriction * DT()
            if self.vVelocity.length() <= vFriction.length():
                self.vVelocity = Vec2()
            else:
                self.vVelocity -= vFriction
        x_max = abs(self.vMaxVelocity.x)
        x_vel = abs(self.vVelocity.x)
        y_max = abs(self.vMaxVelocity.y)
        y_vel = abs(self.vVelocity.y)
        if x_max < x_vel:
           self.vVelocity.x = self.vVelocity.x / x_vel * x_max
        if y_max < y_vel:
           self.vVelocity.y = self.vVelocity.y / y_vel * y_max
        self.Move()
        self.vForce = Vec2()
        self.bDirty = False

    def AddForce(self,vec):
        self.vForce += vec
        self.bDirty = True
    def AddVelocity(self,vec):
        self.vVelocity += vec
        self.bDirty = True
    def SetVelocity(self,vec):
        self.vVelocity = vec
        self.bDirty = True
    def SetForce(self,vec):
        self.vForce = vec
        self.bDirty = True
    def late_update(self):
        self.update_gravity()
        self.update_physics()
    def final_update(self):
        trans = self.GetOwner().GetTransform()
        ground = Vec2()
        from src.Components.camera import GetCurMainCam
        if not self.bIsGround and trans.GetBottom() < 0:
            trans.m_pos.y = trans.m_size.y / 4
            self.vVelocity.y = 0
            self.bIsGround = True
        if not self.bDirty:
            return
        self.update_physics()
