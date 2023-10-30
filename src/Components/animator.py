from src.Components.component import CComponent
from src.Singletons.resourcemgr import CResMgr


class CAnimation:
    def __init__(self,folderName,duration,repeat,animator):
        self.anim_clips = CResMgr().GetAnim(folderName)
        self.num_of_clips = len(self.anim_clips)
        self.frame = 0
        self.accTime = 0
        self.duration = duration
        self.bFinish = False
        self.bRepeat = repeat
        self.animator = animator
    def update(self):
        from src.Singletons.ctimemgr import DT
        if self.bFinish:
            return
        self.accTime += DT()
        if self.accTime >= self.duration:
            self.accTime = 0
            if self.bRepeat:
                self.frame = (self.frame + 1) % self.num_of_clips
            else:
                self.frame += 1
                if self.frame == self.num_of_clips:
                    self.bFinish = True
                    self.frame = self.num_of_clips - 1
    def render(self):
        trans = self.animator.GetOwner().GetTransform()
        self.anim_clips[self.frame].draw(trans.m_pos.x,trans.m_pos.y)
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
        self.state_map = {}
        self.cur_state = None
    def AddAnimState(self,state_name,state):
        self.state_map[state_name] = state
    def update(self):
        self.cur_state.update()
    def late_update(self):
        pass

    def last_update(self):
        pass

    def final_update(self):
        pass

    def render(self):
        self.cur_state.render()
        next_state = self.cur_state.change_state()
        if '' != next_state:
            self.cur_state.exit_state()
            self.cur_state = self.state_map[next_state]
            self.cur_state.enter_state()
