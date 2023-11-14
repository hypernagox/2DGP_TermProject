from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEBUTTONUP, SDL_MOUSEBUTTONDOWN

from src.Singletons.singleton import SingletonBase
from src.struct.vector2 import Vec2


class CKeyMgr(metaclass=SingletonBase):
    def __init__(self):
        self.key_map = {}
        self.mouse_pos = Vec2()
    def Initialize(self):
        pass
    def update(self):
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
            elif eve.type == SDL_MOUSEBUTTONDOWN:
                if eve.key not in self.key_map: continue
                self.key_map[eve.key] = 'TAP'
                self.mouse_pos = Vec2(eve.x,eve.y)

    def GetKeyState(self,key):
        if key not in self.key_map:
            self.key_map[key] = 'NONE'
        return self.key_map[key]
    def GetMousePos(self):
        pass

def GetKey(key):
    return CKeyMgr().GetKeyState(key)

def GetTapAllKeys():
    pass
def GetHoldAllKeys():
    pass
def GetAwayAllKeys():
    pass