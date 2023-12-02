from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEBUTTONUP, SDL_MOUSEBUTTONDOWN

from Singletons.singleton import SingletonBase
from vector2 import Vec2


class CKeyMgr(metaclass=SingletonBase):
    def __init__(self):
        self.key_map = {}
        self.mouse_pos = Vec2()
    def Initialize(self):
        pass
    def update(self):
        from Singletons.core import CCore
        from pico2d import get_events
        for keys in self.key_map.keys():
            if 'AWAY' == self.key_map[keys]:
                self.key_map[keys] = 'NONE'
            elif 'TAP' == self.key_map[keys]:
                self.key_map[keys] = 'HOLD'

        for eve in get_events():
            if eve.type == SDL_KEYDOWN:
                if eve.key not in self.key_map:continue
                if 'HOLD' != self.key_map[eve.key]:
                    self.key_map[eve.key] = 'TAP'
            elif eve.type == SDL_KEYUP:
                self.key_map[eve.key] = 'AWAY'
            from sdl2 import SDL_MOUSEMOTION
            if eve.type == SDL_MOUSEBUTTONDOWN:
                self.key_map[eve.button] = 'TAP'
                self.mouse_pos = self.convert_coordinates(eve.x,eve.y,CCore().height)
            elif eve.type == SDL_MOUSEBUTTONUP:
                self.key_map[eve.button] = 'AWAY'
            elif eve.type == SDL_MOUSEMOTION:
                self.mouse_pos = self.convert_coordinates(eve.x, eve.y, CCore().height)


    def GetKeyState(self,key):
        if key not in self.key_map:
            self.key_map[key] = 'NONE'
        return self.key_map[key]
    def GetMousePos(self):
        return self.mouse_pos

    def convert_coordinates(self,mouse_x, mouse_y, height):
        new_y = height - mouse_y
        return Vec2(mouse_x,new_y)

def GetKey(key):
    return CKeyMgr().GetKeyState(key)
def GetMousePos():
    return CKeyMgr().GetMousePos()
def GetTapAllKeys():
    pass
def GetHoldAllKeys():
    pass
def GetAwayAllKeys():
    pass