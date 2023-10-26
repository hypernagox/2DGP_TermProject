from src.Singletons.singleton import SingletonBase
class CTimeMgr(metaclass=SingletonBase):
    def __init__(self):
        self.prev_time = 0
        self.delta_time = 1
    def Initialize(self):
        from pico2d import get_time
        self.prev_time = get_time()
        self.delta_time = 1
    def update(self):
        from pico2d import get_time
        cur_time = get_time()
        self.delta_time = cur_time - self.prev_time
        self.prev_time = cur_time
    def GetDT(self):
        return self.delta_time

def DT():
    return CTimeMgr().GetDT()