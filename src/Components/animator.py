from component import CComponent
from animation import CAnimation
class CAnimator(CComponent):
    def __init__(self):
        self.obj = None
        self.anim_map = {}
        self.cur_anim = None
    def AddAnim(self,anim_name,folderName):
        self.anim_map[anim_name] = CAnimation(folderName)
