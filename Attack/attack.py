

class CAttack:
    def __init__(self,obj):
        self.obj = obj
        self.ball_count = 10
        self.scale = 1.

    def do_attack(self,ball):
        if self.ball_count <= 0 :
            return False
        from Objects.ball import CBall
        player_pos = self.obj.GetObjectScreenPos()
        from Singletons.ckeymgr import GetMousePos
        mpos = GetMousePos()
        dir = (mpos - player_pos).normalized()
        from Singletons.ckeymgr import GetKey
        if 'HOLD' == GetKey(1) or 'TAP' == GetKey(1):
            from Singletons.ctimemgr import DT
            ball.ready_to_fire = True
            self.scale += 5 * DT()
            from pico2d import clamp
            self.scale = clamp(1,self.scale,3)
            ball.GetTransform().m_scale = self.scale
            ball.item_fire_dir = dir
            return False
        elif 'AWAY' == GetKey(1):
            from Singletons.eventmgr import CreateObj
            scale = self.scale
            CreateObj("PROJ",CBall(50, 50, self.obj.GetTransform().m_pos + dir * 10, dir,scale))
            self.ball_count -= 1
            self.scale = 0
            return True