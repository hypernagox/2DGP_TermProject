import random

from Objects.cobjects import CObject
from vector2 import Vec2

import time

random.seed(time.time())
class CItem(CObject):
    def __init__(self,size,pos,item_img_name):
        super().__init__()

        from copy import deepcopy
        self.GetTransform().m_size = deepcopy(size)
        self.GetTransform().m_pos = deepcopy(pos)
        self.GetTransform().m_finalPos = deepcopy(pos)
        from Components.collider import CCollider
        col = self.AddComponent("Collider",CCollider(self))
        col.m_vSizeOffSet = Vec2(50,50)
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer",CSpriteRenderer(item_img_name))
        from Components.rigidbody import CRigidBody
        rigid = self.AddComponent("RigidBody",CRigidBody())
        rigid.SetVelocity(Vec2(0,1) * 100)
        rigid.bGravity = False
        self.ready_to_fire = False
        self.rev_speed = random.uniform(0.5, 5.5)
        self.item_fire_dir = Vec2(1,1)
        self.acc=0
        self.life = 5
        from Singletons.resourcemgr import GetSound
        self.item_sound = GetSound('item_sound.ogg')
        GetSound('item_create.ogg').play()
    def update(self):
        super().update()
        if None != self.parent:
            if self.ready_to_fire:
                d = self.item_fire_dir * 100.
                self.GetTransform().m_pos = d
            else:
                self.GetTransform().OrbitAroundParent(100,self.rev_speed)
        else:
            from Singletons.ctimemgr import DT
            self.acc += DT()
            if self.acc >= self.life:
                from Singletons.eventmgr import DestroyObj
                DestroyObj(self)
    def render(self):
        super().render()
    def OnCollisionEnter(self,other):
        if other.group_name == "SWORD": return
        if self.parent == None and other.group_name == "TILE":
            self.GetComp("RigidBody").bGravity = True
        if self.parent != None or other.group_name != 'PLAYER':
            return
        from Singletons.cscenemgr import GetCurScene
        self.item_sound.play()
        self.GetComp("RigidBody").bGravity = False
        GetCurScene().remove_object(self)
        other.AddChild(self)
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass
