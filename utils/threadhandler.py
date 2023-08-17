if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from threading import Thread

class DMXThreadHandler():
    """ Threading handler for DMXControl """

    def __init__(self):
        """ Constructs a :class: `DMXThreadHandler <DMXThreadHandler>` """

        self.__threads:list[Thread] = []

    def get(self) -> list[Thread]:
        """ Returns the current threads
        
        :returns: The list of threads
        :rtype: list[Thread]
        """
        
        return self.__threads
    
    def append(self,thread:Thread) -> None:
        """ Appends a thread to the current threads

        :param thread: The thread to append
        :type  thread: Thread
        """

        self.__threads.append(thread)

    def remove(self,thread:Thread) -> None:
        """ Removes a thread to the current threads

        :param thread: The thread to remove
        :type  thread: Thread
        """

        self.__threads.remove(thread)
