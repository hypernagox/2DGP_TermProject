from Singletons.core import CCore


class CFactory:
    @staticmethod
    def CreateObject(object_type,strFolderName = None):
        if 'Player' == object_type:

            from Objects.cplayer import CPlayer
            return CPlayer()
        if 'Monster' == object_type:

            from Objects.monster import CMonster
            return CMonster(strFolderName)

class CLayerFactory:
    @staticmethod
    def CreateLayer(fileName,filelb,filert,worldLeftBottom,width = CCore().width * 2,height = CCore().height * 2):
       from Objects.layer import CLayer
       return CLayer(fileName,filelb,filert,worldLeftBottom,width,height)
