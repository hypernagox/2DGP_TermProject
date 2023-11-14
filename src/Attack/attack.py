

class CAttack:
    def __init__(self,obj):
        self.obj = obj
    def do_attack(self):
        from src.Objects.ball import CBall
        player_pos = self.obj.GetObjectScreenPos()
        from src.Singletons.ckeymgr import GetMousePos
        mpos = GetMousePos()
        dir = (mpos - player_pos).normalized()
        from src.Singletons.eventmgr import CreateObj
        CreateObj("PROJ",CBall(21, 21, self.obj.GetTransform().m_pos + dir * 10, dir))