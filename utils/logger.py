if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from utils.exceptions import LoggerFileNotFoundError
import os,logging,sys

class Logger():
    """ Logging system for DMXControl """
    
    def __init__(self,sessionFile:str="",logFile:str="",formatting:str="[%(asctime)s.%(msecs)03d] [%(levelname)s]: %(message)s",dateTime:str="%m-%d-%Y %H:%M:%S",*a,**k):
        """
        Constructs a :class: 'Logger <Logger>'

        :param sessionFile str:
            (Optional, "") String containing location (path) of the session file used by the main code. Will throw an exception if left empty
        :param logFile str:
            (Optional, "") String containing location (path) of the log file used by the main code. Will throw an exception if left empty
        :param formatting str:
            (Optional, "[%(asctime)s] [%(levelname)s]: %(message)s") String defining the formatting to be used by the logger. Follows the logger module's rules for how it is formatted
        :param dateTime str:
            (Optional, "%m-%d-%Y %H:%M:%S") String defining the formatting of dates and times used by the logger. Follows the logging module's rules for how it is formatted
        :param a list:
            Other arguments passed
        :param k dict:
            Other keyword arguments passed
        """
        
        
        self.os=os
        self.logging=logging
        self.sys=sys
        
        self.sessionFile=sessionFile
        self.logFile=logFile
        self.format="%(message)s"
        self.format=formatting
        self.dateTime=dateTime

        if not os.path.exists(self.sessionFile):
            raise LoggerFileNotFoundError("session",self.sessionFile)

        if not os.path.exists(self.logFile):
            raise LoggerFileNotFoundError("previous log",self.logFile)

        self.logger=logging.getLogger()
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        
        self.loggingFormatter=logging.Formatter(self.format,self.dateTime)
        
        self.loggingStdoutHandler=logging.StreamHandler(self.sys.stdout)
        self.loggingStdoutHandler.setLevel(logging.DEBUG)
        self.loggingStdoutHandler.setFormatter(self.loggingFormatter)

        self.loggingFileHandler=logging.FileHandler(self.logFile)
        self.loggingFileHandler.setLevel(logging.DEBUG)
        self.loggingFileHandler.setFormatter(self.loggingFormatter)

        self.logger.addHandler(self.loggingFileHandler)
        self.logger.addHandler(self.loggingStdoutHandler)

    def clearLog(self,*a,**k):
        """ Clears the log file """
        assert os.path.exists(self.logFile)
        open(self.logFile,"w").close()

    def log(self,msg,*a,**k):
        """
        Logs a message with level LOG

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        
        self.logger.log(msg,*a,*k)

    def debug(self,msg,*a,**k):
        """
        Logs a message with level DEBUG

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.debug(msg,*a,*k)

    def info(self,msg,*a,**k):
        """
        Logs a message with level INFO

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.info(msg,*a,*k)

    def warning(self,msg,*a,**k):
        """
        Logs a message with level WARNING

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.warning(msg,*a,*k)
    
    def error(self,msg,*a,**k):
        """
        Logs a message with level ERROR

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.error(msg,*a,*k)

    def critical(self,msg,*a,**k):
        """
        Logs a message with level CRITICAL

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.critical(msg,*a,*k)

    def exception(self,msg,*a,**k):
        """
        Logs a message with level EXCEPTION

        :param msg str:
            The message to be logged
        :param a list:
            Any other paramaters to be passed to the logger
        :param k dict:
            Any other keyword arguments to be passed to the logger
        """
        self.logger.exception(msg,*a,*k)
