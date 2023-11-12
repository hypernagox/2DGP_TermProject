from src.Components.transform import CTransform


class CObject:
    def __init__(self):
        self.components = []
        self.childs = []
        self.comp_map = {}
        self.name = ''
        self.components.append(CTransform())
        self.components[0].SetOwner(self)
        self.IsDead = False
    def AddComponent(self,comp_name,comp):
        self.components.append(comp)
        self.comp_map[comp_name] = comp
        comp.SetOwner(self)
        return comp
    def AddChild(self,child):
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