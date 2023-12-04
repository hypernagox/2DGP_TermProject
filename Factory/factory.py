from Singletons.core import CCore
from vector2 import Vec2


class CFactory:
    @staticmethod
    def CreateObject(object_type,start_pos = Vec2(0,0),size = Vec2(100,100),strFolderName = None):
        if 'Player' == object_type:

            from Objects.cplayer import CPlayer
            return CPlayer()
        if 'Monster' == object_type:

            from Objects.monster import CMonster
            return CMonster(start_pos,size,strFolderName)

class CLayerFactory:
    @staticmethod
    def CreateLayer(fileName,filelb,filert,worldLeftBottom,width = CCore().width * 2,height = CCore().height * 2):
       from Objects.layer import CLayer
       return CLayer(fileName,filelb,filert,worldLeftBottom,width,height)
