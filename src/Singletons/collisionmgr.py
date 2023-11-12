from singleton import SingletonBase
from src.Scene.cscene import GROUP_NAME
from src.struct.vector2 import Vec2

def RegisterGroup(group_name_a,group_name_b):
    CCollisionMgr().RegisterGroup(group_name_a,group_name_b)
class CCollisionMgr(metaclass = SingletonBase):
    def __init__(self):
        self.collision_table =[[False for _ in range(len(GROUP_NAME))] for _ in range(len(GROUP_NAME))]
        self.map_prev_collision = {}
    def RegisterGroup(self,group_name_a,group_name_b):
        a = GROUP_NAME[group_name_a]
        b = GROUP_NAME[group_name_b]
        if a > b : a,b = b,a
        self.collision_table[a][b] = not self.collision_table[a][b]
    def update_collision(self):
        end_group = len(GROUP_NAME)
        for i in range(end_group):
            for j in range(i + 1,end_group):
                if self.collision_table[i][j]:
                    self.CheckCollision(i,j)
    def CheckCollision(self,row,col):
        from src.Singletons.cscenemgr import GetCurSceneObjects
        objs = GetCurSceneObjects()
        end_group = len(GROUP_NAME)
        for a in objs[row]:
            a_collider = a.GetComp("Collider")
            if a_collider is None:
                continue
            for b in objs[col]:
                b_collider = b.GetComp("Collider")
                if b_collider is None:
                    continue
                left_id = a_collider.m_Collider_ID
                right_id = b_collider.m_Collider_ID
                union_key = (left_id,right_id)
                if union_key not in self.map_prev_collision:
                    self.map_prev_collision[union_key] = False
                now_collision = self.IsCollision(a_collider.obb_box, b_collider.obb_box)
                if now_collision:
                    if self.map_prev_collision[union_key]:
                        if a_collider.IsDeadObj() or b_collider.IsDeadObj():
                            a_collider.OnCollisionExit(b_collider)
                            b_collider.OnCollisionExit(a_collider)
                        else:
                            a_collider.OnCollisionStay(b_collider)
                            b_collider.OnCollisionStay(a_collider)
                    else:
                        if not a_collider.IsDeadObj() and not b_collider.IsDeadObj():
                            a_collider.OnCollisionEnter(b_collider)
                            b_collider.OnCollisionEnter(a_collider)
                else:
                    if not self.map_prev_collision[union_key]:
                        a_collider.OnCollisionExit(b_collider)
                        b_collider.OnCollisionExit(a_collider)

    def IsCollision(self , obb1, obb2):
        axes = []
        corners = obb1.corners
        for i in range(4):
            axis = (corners[i] - corners[(i + 1) % 4]).normalized()
            axes.append(axis)
        corners = obb2.corners
        for i in range(4):
            axis = (corners[i] - corners[(i + 1) % 4]).normalized()
            axes.append(axis)
        for axis in axes:
            if not overlap_on_axis(axis, obb1, obb2):
                return False
        return True

def project_obb_on_axis(obb, axis):
    corners = obb.corners
    min_proj = max_proj = corners[0].dot(axis)
    for corner in corners[1:]:
        projection = corner.dot(axis)
        min_proj = min(min_proj, projection)
        max_proj = max(max_proj, projection)

    return min_proj, max_proj

def overlap_on_axis(axis, obb1, obb2):
    min1, max1 = project_obb_on_axis(obb1, axis)
    min2, max2 = project_obb_on_axis(obb2, axis)
    return max1 >= min2 and max2 >= min1
