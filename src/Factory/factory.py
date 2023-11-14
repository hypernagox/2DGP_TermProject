from src.Singletons.core import CCore


class CFactory:
    @staticmethod
    def CreateObject(object_type):
        if 'Player' == object_type:
            from src.Objects.cplayer import CPlayer
            return CPlayer()
        if 'Monster' == object_type:
            from src.Objects.monster import CMonster
            return CMonster()

class CLayerFactory:
    @staticmethod
    def CreateLayer(fileName,filelb,filert,worldLeftBottom,width = CCore().width * 2,height = CCore().height * 2):
        from src.Objects.layer import CLayer
        return CLayer(fileName,filelb,filert,worldLeftBottom,width,height)
