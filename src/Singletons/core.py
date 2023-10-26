from singleton import SingletonBase
from pico2d import *
class CCore(metaclass = SingletonBase):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.should_close = False
    def Initialize(self):
        open_canvas()
        return
        pass
    def GameLoop(self):
        while not self.should_close:
            update_canvas()
            clear_canvas()
        close_canvas()

