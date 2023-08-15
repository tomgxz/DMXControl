if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from threading import Thread

class DMXThreadHandler():
    def __init__(self):
        self.__threads:list[Thread] = []

    def get(self):
        return self.__threads
    
    def append(self,thread:Thread):
        self.__threads.append(thread)

    def remove(self,thread:Thread):
        self.__threads.remove(thread)
