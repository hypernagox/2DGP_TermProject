from src.Components.component import CComponent
from src.struct.vector2 import Vec2


class CCollider(CComponent):
    g_collider_ID = 0
    def __init__(self,obj):
        super().__init__()
        self.owner = obj
        self.m_transform = obj.GetTransform()
        self.m_Collider_ID = CCollider.g_collider_ID
        CCollider.g_collider_ID += 1
        self.m_vOffset = Vec2()
        self.m_vSizeOffset = Vec2()

    def last_update(self):
        pass

    def OnCollisionEnter(self,other):
        self.owner.OnCollisionEnter(other.owner)
    def OnCollisionStay(self,other):
        self.owner.OnCollisionStay(other.owner)
    def OnCollisionExit(self,other):
        self.owner.OnCollisionExit(other.owner)

class OBB:
    def __init__(self, center, width, height, angle):
        self.center = center
        self.width = width
        self.height = height
        self.angle = angle
        self.corners = self.calculate_corners()
        self.axes = self.calculate_axes()

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
            normal = Vec2(-edge.y, edge.x)  # Perpendicular to the edge
            axes.append(normal.normalized())
        return axes

    def update(self, new_center, new_angle):

        self.center = new_center
        self.angle = new_angle
        self.corners = self.calculate_corners()
        self.axes = self.calculate_axes()

