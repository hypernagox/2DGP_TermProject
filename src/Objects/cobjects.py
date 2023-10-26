
class CObject:
    def __init__(self):
        self.components = []
        self.comp_map = {}
        self.name = ''
    def AddComponent(self,comp_name,comp):
        self.components.append(comp)
        self.comp_map[comp_name] = comp
    def GetComp(self,comp_name):
        return self.comp_map[comp_name]
    def update(self):
        for comp in self.components:
            comp.update()
    def late_update(self):
        for comp in self.components:
            comp.late_update()
    def last_update(self):
        for comp in self.components:
            comp.last_update()
    def final_update(self):
        for comp in self.components:
            comp.final_update()
    def render(self):
        for comp in self.components:
            comp.render()