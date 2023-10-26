class SingletonBase(type):
    g_instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.g_instances:
            instance = super().__call__(*args, **kwargs)
            cls.g_instances[cls] = instance
        return cls.g_instances[cls]