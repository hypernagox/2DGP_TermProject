

class CAttack:
    def __init__(self,obj):
        self.obj = obj
        self.ball_count = 3
    def do_attack(self):
        if self.ball_count <= 0 :
            return
        from src.Objects.ball import CBall
        player_pos = self.obj.GetObjectScreenPos()
        from src.Singletons.ckeymgr import GetMousePos
        mpos = GetMousePos()
        dir = (mpos - player_pos).normalized()
        from src.Singletons.eventmgr import CreateObj
        CreateObj("PROJ",CBall(21, 21, self.obj.GetTransform().m_pos + dir * 10, dir))
        self.ball_count -= 1