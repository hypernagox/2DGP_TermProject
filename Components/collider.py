from Components.component import CComponent
from vector2 import Vec2

g_renderColBox = True

class CCollider(CComponent):
    g_collider_ID = 0
    g_colBox = None
    def __init__(self,obj):
        super().__init__()
        if CCollider.g_colBox == None :
            from Singletons.resourcemgr import CResMgr
            CCollider.g_colBox = CResMgr().GetTex('colbox.png')
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.m_Collider_ID = CCollider.g_collider_ID
        CCollider.g_collider_ID += 1
        self.m_vOffset = Vec2()
        self.m_vSizeOffset = Vec2()
        self.obb_box = OBB(self)
        self.collision_count = 0
        self.cur_col_target = ''
        self.cur_pene = Vec2()
    def last_update(self):
        self.obb_box.update(self.m_transform.m_finalPos ,self.m_transform.m_size + self.m_vSizeOffset
                            ,self.m_transform.m_finalDegree , self.m_vOffset)
    def OnCollisionEnter(self,other):
        self.collision_count += 1
        self.owner.OnCollisionEnter(other.owner)
        self.cur_col_target = other.owner.group_name
        from Singletons.collisionmgr import GetPenetrationVector
        self.cur_pene = GetPenetrationVector(self,other,self)
    def OnCollisionStay(self,other):
        self.owner.OnCollisionStay(other.owner)
    def OnCollisionExit(self,other):
        self.collision_count -= 1
        self.owner.OnCollisionExit(other.owner)
    def GetCollisionDir(self):
        return self.cur_pene
    def GetRigidBody(self):
        return self.owner.GetComp("RigidBody")
    def render(self):
        if not g_renderColBox:
            return
        self.owner.GetComp("SpriteRenderer").render_target(
            CCollider.g_colBox,
            0,
            0,
            512,
            512,
            False,
            self.m_vSizeOffset
        )
    def GetMaxAxisLength(self):
        return self.obb_box.max_length


class OBB:
    def __init__(self,collider):
        self.collider = collider
        self.center = Vec2()
        self.width = 0
        self.height = 0
        self.angle = 0
        self.corners = []
        self.axes = []
        self.max_length = 0
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
        max_squared_length = 0
        axes = []
        for i in range(4):
            edge = self.corners[i] - self.corners[(i + 1) % 4]
            squared_length = edge.x ** 2 + edge.y ** 2
            max_squared_length = max(max_squared_length, squared_length)

            normal = Vec2(-edge.y, edge.x)
            axes.append(normal.normalized())

        return axes, max_squared_length

    def update(self, center,size,angle,offset):
        self.center = center + offset
        self.angle = angle
        self.width = size.x
        self.height = size.y
        self.corners = self.calculate_corners()
        self.axes,self.max_length = self.calculate_axes()


