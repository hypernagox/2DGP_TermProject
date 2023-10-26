from src.Components.component import CComponent
from src.Singletons.resourcemgr import CResMgr


class CAnimation:
    def __init__(self,folderName):
        self.anim_clips = CResMgr().GetAnim(folderName)
        self.num_of_clips = len(self.anim_clips)
        self.frame = 0
    def update(self):
        self.frame = (self.frame + 1) % self.num_of_clips
    def render(self):
        self.anim_clips[self.frame].draw(100,100)
class CState:
    def update(self):
        pass
    def enter_state(self):
        pass
    def exit_state(self):
        pass
    def change_state(self):
        pass

class CAnimator(CComponent):
    def __init__(self):
        super().__init__()
        self.obj = None
        self.anim_map = {}
        self.state_map = {}
        self.cur_anim = None
        self.cur_state = None
    def AddAnimState(self,anim_name,folderName,state):
        self.anim_map[anim_name] = CAnimation(folderName)
        self.state_map[anim_name] = state
    def update(self):
        self.cur_anim.update()
        self.cur_state.update()
    def late_update(self):
        pass

    def last_update(self):
        pass

    def final_update(self):
        pass

    def render(self):
        self.cur_anim.render()
        next_state =  self.cur_state.change_state()
        if '' != next_state:
            self.cur_state.exit_state()
            self.cur_state = self.state_map[next_state]
            self.cur_state.enter_state()
            self.cur_anim = self.anim_map[next_state]
