from singleton import SingletonBase

from pathlib import Path
from singleton import SingletonBase
class CPathMgr(metaclass=SingletonBase):
    def __init__(self):
        self.res_path = None
        self.texture_path = None
        self.sound_path = None

    def Initialize(self):
        self.res_path = Path(__file__).resolve().parent.parent.parent / 'Resource'
        self.texture_path = self.res_path / 'Texture'
        self.sound_path = self.res_path / 'Sound'
        self.anim_path = Path(__file__).resolve().parent.parent.parent / 'Animations'
    def GetTexPath(self):
        return self.texture_path
    def GetSoundPath(self):
        return self.sound_path
    def GetResPath(self):
        return self.res_path
    def GetAnimPath(self):
        return self.anim_path

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