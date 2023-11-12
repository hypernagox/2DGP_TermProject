class CFactory:
    @staticmethod
    def CreateObject(object_type):
        if 'Player' == object_type:
            from src.Objects.cplayer import CPlayer
            return CPlayer()
        if 'Monster' == object_type:
            from src.Objects.monster import CMonster
            return CMonster()