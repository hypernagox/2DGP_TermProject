class CFactory:
    @staticmethod
    def CreateObject(object_type):
        if 'Player' == object_type:
            from src.Objects.cplayer import CPlayer
            return CPlayer()
        pass