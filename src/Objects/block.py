from src.Objects.cobjects import CObject


class CBlock(CObject):
    def __init__(self,x,y,size):
        super().__init__()
        from src.struct.vector2 import Vec2
        self.GetTransform().m_pos = Vec2(x,y)
        self.GetTransform().m_size = size
        from src.Components.collider import CCollider
        self.AddComponent("Collider",CCollider(self))
        from src.Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer("brick.png"))

    def update(self):
        print(self.GetTransform().m_pos.x)
    def OnCollisionEnter(self,other):
        from src.Singletons.collisionmgr import GetPenetrationVector
        penetration = GetPenetrationVector(self.GetComp("Collider"),other.GetComp("Collider"),other.GetComp("Collider"))
        from src.struct.vector2 import Vec2
        other.GetTransform().m_pos -= penetration
        other.GetComp("RigidBody").ResetPhysics()
        other.GetComp("RigidBody").bIsGround = True
    def OnCollisionStay(self,other):
        from src.Singletons.collisionmgr import GetPenetrationVector
        penetration = GetPenetrationVector(self.GetComp("Collider"), other.GetComp("Collider"),
                                           other.GetComp("Collider"))
        from src.struct.vector2 import Vec2
        other.GetTransform().m_pos -= penetration
        other.GetComp("RigidBody").ResetPhysics()
        other.GetComp("RigidBody").bIsGround = True
        pass
    def OnCollisionExit(self,other):
        #other.GetComp("RigidBody").bIsGround = False
        pass


