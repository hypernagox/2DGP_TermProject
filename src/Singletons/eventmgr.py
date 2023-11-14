from src.Singletons.singleton import SingletonBase


class CEventMgr(metaclass=SingletonBase):
    def __init__(self):
        self.event_lists = []
        self.coroutine_lists =[]
        self.coroutine_map = {}
    def update(self):
        for event in self.event_lists:
            event.accept()
        for coro in self.coroutine_lists:
            pass
        for coro in self.coroutine_map.values():
            pass
        self.event_lists.clear()

def AddEvent(eve):
    CEventMgr().event_lists.append(eve)

def StartCoRoutine(coro):
    CEventMgr().coroutine_lists.append(coro)

def StartCoRoutineWithKey(coro_name,coro):
    CEventMgr().coroutine_map[coro_name] = coro

def CreateObj(group_name,obj):
    AddEvent(CreateObjEvent(group_name,obj))
def DestroyObj(obj):
    AddEvent(DestroyObjEvent(obj))
class CEvent:
    def accept(self):
        pass
class CreateObjEvent(CEvent):
    def __init__(self,group_name,obj):
        self.group_name = group_name
        self.obj = obj
    def accept(self):
        from src.Singletons.cscenemgr import CSceneMgr
        CSceneMgr().GetCurScene().AddObject(self.group_name,self.obj)
class DestroyObjEvent(CEvent):
    def __init__(self,obj):
        self.obj = obj
    def accept(self):
        self.obj.IsDead = True