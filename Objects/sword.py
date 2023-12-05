from Components.collider import CCollider
from Objects.cobjects import CObject
from vector2 import Vec2


class CSword(CObject):
    def __init__(self,obj):
        super().__init__()
        self.obj = obj
        col = self.AddComponent("Collider", CCollider(self))
        self.GetTransform().m_pos = Vec2(0,0)
        self.GetTransform().m_size = Vec2(200,100)
        #col.m_vSizeOffset = Vec2(300,200)
        self.bActivate = False
        from Singletons.cscenemgr import GetCurScene
        GetCurScene().AddObject("SWORD",self)
        from Components.spriterenderer import CSpriteRenderer
        self.AddComponent("SpriteRenderer", CSpriteRenderer())
    # def update(self):
    #     from copy import deepcopy
    #     self.GetTransform().m_pos = deepcopy(self.obj.GetTransform().m_finalPos)
    # def render(self):
    #     print(self.GetTransform().m_pos.x, self.GetTransform().m_pos.y)
    #     return
    def OnCollisionEnter(self,other):
        from Singletons.eventmgr import DestroyObj
        if other.name == "boss_block":return
        if self.bActivate:
            if other.group_name == 'MONSTER' or other.group_name == 'FLYING_MONSTER':
                rigid = other.GetComp("RigidBody")
                rigid.SetVelocity(rigid.GetVelocity().normalized() * -1)
            else:
                DestroyObj(other)
       # print('칼')
    def OnCollisionStay(self,other):
        from Singletons.eventmgr import DestroyObj
        if other.name == "boss_block": return
        #if other.group_name == 'MONSTER' or other.group_name == 'FLYING_MONSTER':return
        if self.bActivate:
            if other.group_name == 'MONSTER' or other.group_name == 'FLYING_MONSTER':
                rigid = other.GetComp("RigidBody")
                rigid.SetVelocity(rigid.GetVelocity().normalized() * -10000)
            else:
                DestroyObj(other)



    def OnCollisionExit(self,other):
        from Singletons.eventmgr import DestroyObj
        if other.name == "boss_block": return
        if other.group_name == 'MONSTER' or other.group_name == 'FLYING_MONSTER': return
        if self.bActivate:
            DestroyObj(other)
            from Objects.item import CItem
            item = CItem(Vec2(30, 30), self.GetTransform().m_finalPos, "ball21x21.png")
            from Singletons.eventmgr import CreateObj
            CreateObj("ITEM", item)
            item.GetComp("RigidBody").bGravity = True


