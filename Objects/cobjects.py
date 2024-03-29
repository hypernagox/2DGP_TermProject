from Components.transform import CTransform


class CObject:
    def __init__(self):
        self.components = []
        self.parent = None
        self.group_name = None
        self.childs = []
        self.comp_map = {}
        self.name = ''
        self.components.append(CTransform())
        self.components[0].SetOwner(self)
        self.IsDead = False
        self.hp = 10000

    def DecreaseHP(self,decrease_val):
        self.hp -= decrease_val
    def AddComponent(self,comp_name,comp):
        self.components.append(comp)
        self.comp_map[comp_name] = comp
        comp.SetOwner(self)
        return comp

    def EraseChild(self,obj):
        self.GetTransform().childs.remove(obj.GetTransform())
        self.childs.remove(obj)
    def AddChild(self,child):
        child.parent = self
        self.childs.append(child)
        self.components[0].AddChild(child.components[0])
    def GetTransform(self):
        return self.components[0]
    def GetComp(self,comp_name):
        if comp_name not in self.comp_map: return None
        return self.comp_map[comp_name]
    def update(self):
        for comp in self.components:
            comp.update()
        for childs in self.childs:
            childs.update()
    def late_update(self):
        for comp in self.components:
            comp.late_update()
        for childs in self.childs:
            childs.late_update()
    def last_update(self):
        for comp in self.components:
            comp.last_update()
        for childs in self.childs:
            childs.last_update()
    def final_update(self):
        for comp in self.components:
            comp.final_update()
        for childs in self.childs:
            childs.final_update()
    def render(self):
        for comp in self.components:
            comp.render()
        for childs in self.childs:
            childs.render()
    def OnCollisionEnter(self,other):
        pass
    def OnCollisionStay(self,other):
        pass
    def OnCollisionExit(self,other):
        pass

    def GetObjectScreenPos(self):
        from Components.camera import GetCurMainCam
        return GetCurMainCam().world_to_screen(self.GetTransform().m_pos)

    class _ObjectIterator:
        def __init__(self, root):
            self.stack = [root]

        def __iter__(self):
            return self

        def __next__(self):
            if not self.stack:
                raise StopIteration

            node = self.stack.pop()
            self.stack.extend(reversed(node.childs))
            return node

    def __iter__(self):
        return CObject._ObjectIterator(self)