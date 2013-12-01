class __getSingleton:
    def __init__(self, cls):
        self.__cls=cls
        self.__instance=None
        
    def __call__(self):
        if not self.__instance:
            self.__instance=self.__cls.__new__(self.__cls, True)
        
        return self.__instance
    
    def __del__(self):
        del self.__cls
        del self.__instance


class Singleton(object):
    def __new__(cls, ok=False, *args, **kargs):
        if not ok:
            raise SingletonError, "This class is a singleton, and can't be created using the standard constructor"
        else:
            newobj=object.__new__(cls)
            newobj.__init__(*args, **kargs)
            return newobj
        
    def __init__(self):
        object.__init__(self)


class SingletonError(Exception):
    pass

        
if __name__=="__main__":
    getSingleton=__getSingleton(Singleton)        

