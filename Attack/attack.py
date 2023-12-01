

class CAttack:
    def __init__(self,obj):
        self.obj = obj
        self.ball_count = 3
        self.scale = 1.

    def do_attack(self,ball):
        if self.ball_count <= 0 :
            return False
        from Singletons.ckeymgr import GetKey
        if 'HOLD' == GetKey(1) or 'TAP' == GetKey(1):
            from Singletons.ctimemgr import DT
            #ball.ready_to_fire = True
            self.scale += 5 * DT()
            from pico2d import clamp
            self.scale = clamp(self.scale,1,2)
            #ball.GetTransform().m_scale = self.scale
            return False
        elif 'AWAY' == GetKey(1):
            from Objects.ball import CBall
            player_pos = self.obj.GetObjectScreenPos()
            from Singletons.ckeymgr import GetMousePos
            mpos = GetMousePos()
            dir = (mpos - player_pos).normalized()
            from Singletons.eventmgr import CreateObj
            CreateObj("PROJ",CBall(21*self.scale, 21*self.scale, self.obj.GetTransform().m_pos + dir * 10, dir))
            self.ball_count -= 1
            self.scale = 0
            return True