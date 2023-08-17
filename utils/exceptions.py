from data import strings

class ModuleRunError(Exception):
    def __init__(self):
        """ Prevents modules for being called without the main application """

        super().__init__(strings.GENERIC_MODULE_RUN_ERROR)

if __name__ == "__main__":
    raise ModuleRunError()

class LoggerException(Exception):
    def __init__(self,message):
        """ Common base class for all Logger exceptions """

        super().__init__(message)

class LoggerExceptionHandlingError(LoggerException):
    def __init__(self):
        """ Error in the handling of a Logger exception """

        super().__init__(strings.LOGGER_EXCEPTIONHANDLINGERROR)

class LoggerFileNotFoundError(LoggerException):
    def __init__(self,file:str="",url:str=""):
        """ Logger file not found """

        try:
            assert type(file) == str
            assert type(url) == str
            assert file not in [""]
            assert url not in [""]
        except AssertionError as exec:
            raise LoggerExceptionHandlingError

        super().__init__(strings.LOGGER_FILENOTFOUND.format(file,url))

class InterfaceException(Exception):
    def __init__(self,message):
        """  """

        super().__init__(message)

class InterfaceFailedConnectionException(InterfaceException):
    def __init__(self):
        """ Common base class for all DMX Interface exceptions """

        super().__init__(strings.INTERFACE_FAILED_CONNECTION)

class InterfaceAbortConnectionException(InterfaceException):
    def __init__(self,message:str = ""):
        """ Interface connection aborted after some amount of attempts """

        super().__init__(strings.INTERFACE_ABORT_CONNECTION if message == "" else message)

class InterfaceDisconnectedException(InterfaceException):
    def __init__(self):
        """ Interface disconnected """

        super().__init__(strings.INTERFACE_DISCONNECTED)

class InterfaceNotConnectedException(InterfaceException):
    def __init__(self):
        """ Interface not connected """

        super().__init__(strings.INTERFACE_NOT_CONNECTED)

class InterfaceInvalidArgumentException(InterfaceException):
    def __init__(self, message):
        """ Invalid argument passed """

        super().__init__(strings.GENERIC_INVALID_ARGUMENT.format(message))