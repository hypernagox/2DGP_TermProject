from ..Singletons.pathmgr import CPathMgr
class CAnimation:
    def __init__(self,folderName):
        self.anim_clips = []
        target_dir = CPathMgr().GetAnimPath() / folderName
        for clips in target_dir.rglob('*'):
            if clips.is_file():
                from pico2d import load_image
                self.anim_clips.append(load_image(str(clips.absolute())))
        self.num_of_clips = len(self.anim_clips)
