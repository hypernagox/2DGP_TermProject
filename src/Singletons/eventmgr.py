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