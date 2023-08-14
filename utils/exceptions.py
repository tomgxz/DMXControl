class ModuleRunError(Exception):
    def __init__(self):
        super().__init__("This module is to be used in conjunction with the DMXControl application and not as a standalone module.")

if __name__ == "__main__":
    raise ModuleRunError()

class LoggerException(Exception):
    """ Common base class for all Logger exception """

    def __init__(self,message):
        super().__init__(message)

class LoggerExceptionHandlingError(LoggerException):
    """ Common base class for all Logger exception """

    def __init__(self):
        message = f"An exception occured during the handling of another Logger exception."
        super().__init__(message)

class LoggerFileNotFoundError(LoggerException):
    def __init__(self,file:str="",url:str=""):
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
        super().__init__(message)

class InterfaceFailedConnectionException(InterfaceException):
    def __init__(self):
        super().__init__(f"Could not connect to RS-485 DMX Interface.")

class InterfaceAbortConnectionException(InterfaceException):
    def __init__(self,message:str = ""):
        super().__init__(f"Could not connect to RS-485 DMX Interface." if message == "" else message)

class InterfaceDisconnectedException(InterfaceException):
    def __init__(self):
        super().__init__(f"RS-485 DMX Interface disconnected.")

class InterfaceNotConnectedException(InterfaceException):
    def __init__(self):
        super().__init__(f"Interface must be connected to send data.")

class InterfaceInvalidArgumentException(InterfaceException):
    def __init__(self, message):
        super().__init__(f"Invalid argument: {message}")