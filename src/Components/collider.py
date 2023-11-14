from src.Components.component import CComponent
from src.struct.vector2 import Vec2

class CCollider(CComponent):
    g_collider_ID = 0
    g_colBox = None
    def __init__(self,obj):
        super().__init__()
        if CCollider.g_colBox == None :
            from src.Singletons.resourcemgr import CResMgr
            CCollider.g_colBox = CResMgr().GetTex('colbox.png')
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.m_Collider_ID = CCollider.g_collider_ID
        CCollider.g_collider_ID += 1
        self.m_vOffset = Vec2()
        self.m_vSizeOffset = Vec2()
        self.obb_box = OBB()
        self.collision_count = 0
    def last_update(self):
        self.obb_box.update(self.m_transform.m_pos ,self.m_transform.m_size + self.m_vSizeOffset
                            ,self.m_transform.m_degree , self.m_vOffset)
    def OnCollisionEnter(self,other):
        self.collision_count += 1
        self.owner.OnCollisionEnter(other.owner)
    def OnCollisionStay(self,other):
        self.owner.OnCollisionStay(other.owner)
    def OnCollisionExit(self,other):
        self.collision_count -= 1
        self.owner.OnCollisionExit(other.owner)
    def GetRigidBody(self):
        return self.owner.GetComp("RigidBody")
    def render(self):
        self.owner.GetComp("SpriteRenderer").render_target(
            CCollider.g_colBox,
            0,
            0,
            512,
            512,
            False
        )


class OBB:
    def __init__(self):
        self.center = Vec2()
        self.width = 0
        self.height = 0
        self.angle = 0
        self.corners = []
        self.axes = []

    def calculate_corners(self):
        half_width = self.width / 2
        half_height = self.height / 2

        local_corners = [
            Vec2(-half_width, -half_height),
            Vec2(half_width, -half_height),
            Vec2(half_width, half_height),
            Vec2(-half_width, half_height)
        ]

        rotated_corners = [corner.rotate(self.angle) + self.center for corner in local_corners]
        return rotated_corners

    def calculate_axes(self):
        axes = []
        for i in range(4):
            edge = self.corners[i] - self.corners[(i + 1) % 4]
            normal = Vec2(-edge.y, edge.x)
            axes.append(normal.normalized())
        return axes

    def update(self, center,size,angle,offset):
        self.center = center + offset
        self.angle = angle
        self.width = size.x
        self.height = size.y
        self.corners = self.calculate_corners()
        self.axes = self.calculate_axes()


