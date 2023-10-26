from singleton import SingletonBase
from pathmgr import CPathMgr
from core import CCore

class CResMgr(metaclass=SingletonBase):
    def __init__(self):
        self.tex_map = {}
        self.sound_map = {}

    def Initialize(self):
        for tex in CPathMgr().GetTexPath().rglob('**/*'):
            if tex.is_file():
                from pico2d import load_image
                self.tex_map[tex.parent.name + '_' + tex.name] = load_image(str(tex.absolute()))
    def GetTex(self,name):
        return self.tex_map[name]
    def GetSound(self,name):
        return self.sound_map[name]

CCore(800,600).Initialize()
CPathMgr().Initialize()
CResMgr().Initialize()
for name in CResMgr().tex_map.keys():
    print(name)