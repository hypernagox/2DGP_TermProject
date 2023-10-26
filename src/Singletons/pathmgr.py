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