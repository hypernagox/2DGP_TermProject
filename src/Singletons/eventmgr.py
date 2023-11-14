from src.Singletons.singleton import SingletonBase


class CEventMgr(metaclass=SingletonBase):
    def __init__(self):
        self.event_lists = []
        self.coroutine_lists =[]
        self.coroutine_map = {}
    def update(self):
        for event in self.event_lists:
            pass
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
    AddEvent(CreateObj(group_name,obj))

class CEvent:
    def accept(self):
        pass
class CreateObj:
    def __init__(self,obj,group_name):
        self.obj = obj
        self.group_name = group_name
    def accept(self):
        from src.Singletons.cscenemgr import CSceneMgr
        CSceneMgr().GetCurScene().AddObject(self.group_name,self.obj)
