from singleton import SingletonBase
from pathmgr import CPathMgr
from core import CCore

class CResMgr(metaclass=SingletonBase):
    def __init__(self):
        self.tex_map = {}
        self.sound_map = {}

    def Initialize(self):
        for tex in CPathMgr().GetTexPath().rglob('**/*'):
            print(tex)
            if tex.is_file():
                from pico2d import load_image
                self.tex_map[tex.name] = load_image(tex.absolute)
                print(tex)

CCore(800,600).Initialize()
CPathMgr().Initialize()
CResMgr().Initialize()
for name in CResMgr().tex_map.keys():
    print(name)