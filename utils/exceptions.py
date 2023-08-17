class ModuleRunError(Exception):
    def __init__(self):
        """ Prevents modules for being called without the main application """

        super().__init__("This module is to be used in conjunction with the DMXControl application and not as a standalone module.")

if __name__ == "__main__":
    raise ModuleRunError()

class LoggerException(Exception):
    def __init__(self,message):
        """ Common base class for all Logger exceptions """

        super().__init__(message)

class LoggerExceptionHandlingError(LoggerException):
    def __init__(self):
        """ Error in the handling of a Logger exception """

        message = "An exception occured during the handling of another Logger exception."
        super().__init__(message)

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

        message = f"Logging {file} file not found at URL: {url}"
        super().__init__(message)

class InterfaceException(Exception):
    def __init__(self,message):
        """  """

        super().__init__(message)

class InterfaceFailedConnectionException(InterfaceException):
    def __init__(self):
        """ Common base class for all DMX Interface exceptions """

        super().__init__("Could not connect to RS-485 DMX Interface.")

class InterfaceAbortConnectionException(InterfaceException):
    def __init__(self,message:str = ""):
        """ Interface connection aborted after some amount of attempts """

        super().__init__("Could not connect to RS-485 DMX Interface." if message == "" else message)

class InterfaceDisconnectedException(InterfaceException):
    def __init__(self):
        """ Interface disconnected """

        super().__init__("RS-485 DMX Interface disconnected.")

class InterfaceNotConnectedException(InterfaceException):
    def __init__(self):
        """ Interface not connected """

        super().__init__("Interface must be connected to send data.")

class InterfaceInvalidArgumentException(InterfaceException):
    def __init__(self, message):
        """ Invalid argument passed """

        super().__init__(f"Invalid argument: {message}")