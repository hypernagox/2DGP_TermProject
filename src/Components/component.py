
class CComponent:
    def __init__(self):
        self.owner = None
    def set_owner(self,obj):
        self.owner = obj
    def update(self):
        pass
    def late_update(self):
        pass
    def last_update(self):
        pass
    def final_update(self):
        pass
    def render(self):
        pass
    def GetOwner(self):
        return self.owner