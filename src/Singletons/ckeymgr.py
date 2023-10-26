from sdl2 import SDL_KEYDOWN, SDL_KEYUP

from src.Singletons.singleton import SingletonBase
class CKeyMgr(metaclass=SingletonBase):
    def __init__(self):
        self.key_map = {}
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
                self.key_map[eve.key] = 'TAP'
            elif eve.type == SDL_KEYUP:
                self.key_map[eve.key] = 'AWAY'

    def GetKeyState(self,key):
        if key not in self.key_map:
            self.key_map[key] = 'NONE'
        return self.key_map[key]

def GetKey(key):
    return CKeyMgr().GetKeyState(key)