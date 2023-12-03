import pico2d


from Scene.cscene import GROUP_NAME
from Singletons.singleton import SingletonBase
from vector2 import Vec2, dot

EPSILON = 0

def RegisterGroup(group_name_a,group_name_b):
    CCollisionMgr().RegisterGroup(group_name_a,group_name_b)
class CCollisionMgr(metaclass = SingletonBase):
    def __init__(self):
        self.collision_table =[[False for _ in range(len(GROUP_NAME))] for _ in range(len(GROUP_NAME))]
        self.map_prev_collision = {}
        self.map_mtv = {}
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
    def resolve_collision(self,fixed_obj,target_obj,set_ground):
        penetration = GetPenetrationVector(fixed_obj.GetComp("Collider"), target_obj.GetComp("Collider"),
                                           target_obj.GetComp("Collider"))
        #target_obj.GetTransform().m_pos -= penetration

        #target_obj.GetComp("RigidBody").AddVelocity(penetration * -1)
        #col_dir = Vec2()
        collider_size_offset = target_obj.GetComp("Collider").m_vSizeOffset/2

        col_dir = Vec2()

        if abs(penetration.x) > abs(penetration.y):
            if penetration.x > 0:
                if fixed_obj.group_name == 'GROUND':
                    return Vec2(), Vec2()
                col_dir = Vec2(-1, 0)
                new_x_position = fixed_obj.GetTransform().GetLeft() - target_obj.GetTransform().m_size.x / 2 - collider_size_offset.x
            else:
                col_dir = Vec2(1, 0)
                new_x_position = fixed_obj.GetTransform().GetRight() + target_obj.GetTransform().m_size.x / 2 + collider_size_offset.x
            target_obj.GetTransform().m_pos = Vec2(new_x_position, target_obj.GetTransform().m_pos.y)
        else:
            if penetration.y > 0:
                col_dir = Vec2(0, -1)
                new_y_position = fixed_obj.GetTransform().GetBottom() - target_obj.GetTransform().m_size.y / 2 - collider_size_offset.y
            else:
                col_dir = Vec2(0, 1)
                new_y_position = fixed_obj.GetTransform().GetTop() + target_obj.GetTransform().m_size.y / 2 + collider_size_offset.y - 1
            target_obj.GetTransform().m_pos = Vec2(target_obj.GetTransform().m_pos.x, new_y_position)

        target_obj.GetComp("RigidBody").bIsGround = set_ground
        return penetration, col_dir
    def CheckCollision(self,row,col):
        from Singletons.cscenemgr import GetCurSceneObjects
        objs = GetCurSceneObjects()
        end_group = len(GROUP_NAME)
        for a_root in objs[row]:
            for a in a_root:
                if a.group_name == None or row != GROUP_NAME[a.group_name]:continue
                a_collider = a.GetComp("Collider")
                if a_collider is None:
                    continue
                for b_root in objs[col]:
                    for b in b_root:
                        if b.group_name == None or col != GROUP_NAME[b.group_name]: continue
                        b_collider = b.GetComp("Collider")
                        if b_collider is None:
                            continue
                        left_id = a_collider.m_Collider_ID
                        right_id = b_collider.m_Collider_ID
                        union_key = (left_id, right_id)
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
                            if self.map_prev_collision[union_key]:
                                a_collider.OnCollisionExit(b_collider)
                                b_collider.OnCollisionExit(a_collider)

                        self.map_prev_collision[union_key] = now_collision


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
        smallest_overlap = float('inf')
        smallest_axis = None

        for axis in axes:
            overlap = overlap_on_axis(axis, obb1, obb2)
            if overlap <= EPSILON:
                return False
            elif overlap < smallest_overlap:
                smallest_overlap = overlap
                smallest_axis = axis

        if smallest_axis is not None:
            direction = 1 if dot(smallest_axis, obb2.center - obb1.center) > 0 else -1
            mtv_a = smallest_axis * smallest_overlap * direction
            mtv_b = mtv_a * -1
            self.map_mtv[(obb1.collider.m_Collider_ID,obb2.collider.m_Collider_ID)] = {
                obb1.collider.m_Collider_ID: mtv_a,
                obb2.collider.m_Collider_ID: mtv_b
            }
            return True
        else:
            return False
    def GetPenetrationVector(self,colA,colB,col):
        union_key = (colA.m_Collider_ID,colB.m_Collider_ID)
        if union_key in self.map_mtv:
            return self.map_mtv[union_key][col.m_Collider_ID];
        else:
            union_key_rev = (colB.m_Collider_ID,colA.m_Collider_ID)
            return self.map_mtv[union_key_rev][col.m_Collider_ID];

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
    return min(max1, max2) - max(min1, min2)


def GetPenetrationVector(colA,colB,col):
    return CCollisionMgr().GetPenetrationVector(colA,colB,col)


def resolve_collision(fixed_obj, target_obj,set_ground = False):
    return CCollisionMgr().resolve_collision(fixed_obj,target_obj,set_ground)
