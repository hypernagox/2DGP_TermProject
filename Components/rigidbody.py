from Components.component import CComponent
from Singletons.ctimemgr import DT
from vector2 import Vec2


class CRigidBody(CComponent):
    def __init__(self):
        super().__init__()
        self.vForce = Vec2()
        self.vAccel = Vec2()
        self.vVelocity = Vec2()
        self.vMaxVelocity = Vec2(500,1000)
        self.fMass = 1
        self.fFriction = 200
        self.bGravity = True
        self.bIsGround = False
        self.bDirty = True
    def SetIsGround(self,b):
        self.bIsGround = b
        if self.bIsGround:
            self.vAccel.y = 0
            self.vVelocity.y = 0
        else:
            self.GetOwner().GetTransform().m_pos.y += 1
        self.bDirty = True
    def GetVelocity(self):
        return self.vVelocity
    def Move(self):
        trans = self.GetOwner().GetTransform()
        val = abs(self.vVelocity.x)
        if val != 0:
            trans.dir = self.vVelocity.x / val
        trans.m_posOffset += self.vVelocity * DT()
    def update_gravity(self):
        if self.bGravity and not self.bIsGround:
            self.AddForce(Vec2(0,-700))

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
    def ResetY(self):
        self.vAccel.y = self.vForce.y = self.vVelocity.y = 0
    def ResetX(self):
        self.vAccel.x = self.vForce.x = self.vVelocity.x = 0
    def ResetPhysics(self):
        self.vAccel = Vec2()
        self.vVelocity = Vec2()
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
        if self.bGravity and self.bIsGround:
            self.vAccel.y = 0
            self.vForce.y = 0
            self.vVelocity.y = 0
        if not self.bDirty:
            return
        self.update_physics()
