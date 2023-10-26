
class CObject:
    def __init__(self):
        self.components = []
        self.name = ''
    def AddComponent(self,comp):
        self.components.append(comp)
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