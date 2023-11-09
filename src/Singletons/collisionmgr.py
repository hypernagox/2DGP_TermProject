from singleton import SingletonBase
from src.Scene.cscene import GROUP_NAME
class CCollisionMgr(metaclass = SingletonBase):
    def __init__(self):
        pass
    def update_collision(self):
        p = GROUP_NAME["PLAYER"]
