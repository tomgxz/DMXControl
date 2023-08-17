if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

import os,logging,sys

from data import strings
from utils.exceptions import LoggerFileNotFoundError

class DMXLogger():
    """ Logging system for DMXControl """
    
    def __init__(self,sessionFile:str="",logFile:str="",formatting:str="[%(asctime)s.%(msecs)03d] [%(levelname)s]: %(message)s",dateTime:str="%m-%d-%Y %H:%M:%S"):
        """ Constructs a :class: `DMXLogger <DMXLogger>`

        :param sessionFile: (Optional, "") String containing location (path) of the session file used by the main code. Will throw an exception if left empty
        :type  sessionFile: str
        
        :param logFile: (Optional, "") String containing location (path) of the log file used by the main code. Will throw an exception if left empty
        :type  logFile: str
        
        :param formatting: (Optional, "[%(asctime)s] [%(levelname)s]: %(message)s") String defining the formatting to be used by the logger. Follows the logger module's rules for how it is formatted
        :type  formatting: str
        
        :param dateTime: (Optional, "%m-%d-%Y %H:%M:%S") String defining the formatting of dates and times used by the logger. Follows the logging module's rules for how it is formatted
        :type  dateTime: str
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

    def clearLog(self):
        """ Clears the log file """

        assert os.path.exists(self.logFile)
        open(self.logFile,"w").close()

    def log(self,msg,*a,**k):
        """
        Logs a message with level LOG

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        
        self.logger.log(msg,*a,*k)

    def debug(self,msg,*a,**k):
        """
        Logs a message with level DEBUG

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.debug(msg,*a,*k)

    def info(self,msg,*a,**k):
        """
        Logs a message with level INFO

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.info(msg,*a,*k)

    def warning(self,msg,*a,**k):
        """
        Logs a message with level WARNING

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.warning(msg,*a,*k)
    
    def error(self,msg,*a,**k):
        """
        Logs a message with level ERROR

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.error(msg,*a,*k)

    def critical(self,msg,*a,**k):
        """
        Logs a message with level CRITICAL

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.critical(msg,*a,*k)

    def exception(self,msg,*a,**k):
        """
        Logs a message with level EXCEPTION

        :param msg: The message to be logged
        :type  msg: str
        
        :param a: Other arguments passed
        :type  k: list[Any]
        
        :param k: Other keyword arguments passed
        :type  k: dict[str,Any]
        """
        self.logger.exception(msg,*a,*k)

def initialize_logger(sessionfile,logfile):
    """ Initialises the logger and resets the log and session file

    :returns: The DMXLogger object
    :rtype: `DMXLogger <DMXLogger>`
    """

    commands=[] # used to store log commands before the log has been generated, so that they can be appended

    if os.path.exists(sessionfile) and os.path.exists(logfile): # if both files exist, session.txt and latest.log
        with open(sessionfile,"r") as f:
            lines=f.read()
            if lines == "": # if there are no lines in the file
                commands.append(lambda:logger.warning(strings.LOGGER_SESSION_EMPTY))
                previousSessionData={}
            else:
                previousSessionData={line.split(":")[0]:line.split(":")[1] for line in [x.strip("\n") for x in lines.split("\n")]}

        open(sessionfile,"w").close() # clear file

        logFileInt=1
        logFileName=None
        try:
            logFileName=f"data/log/{previousSessionData['datecreated']}-%.log"
        except KeyError as e: # no attribute found in the session data
            commands.append(lambda:logger.warning(strings.LOGGER_SESSION_NODATE))
        else:
            while True:
                if os.path.exists(logFileName.replace("%",str(logFileInt))):
                    logFileInt+=1
                else:
                    break

            with open(logfile,"r") as f1:
                with open(logFileName.replace("%",str(logFileInt)),"w") as f2:
                    f2.write(f1.read())

        open(logfile,"w").close() # clear file

    elif os.path.exists(sessionfile) and not(os.path.exists(logfile)): # if latest.log doesnt exist
        commands.append(lambda:logger.warning(strings.LOGGER_PREVLOG_NOFILE))
        if not os.path.exists("data/log/"):
            os.makedirs("data/log/")
        open(logfile,"w").close()

    elif (not os.path.exists(sessionfile)) and (not os.path.exists(logfile)): # if neither exists
        commands.append(lambda:logger.warning(strings.LOGGER_PREVLOG_NOFILE))
        commands.append(lambda:logger.warning(strings.LOGGER_SESSION_NOFILE))

        # clear both files
        open(logfile,"w").close()
        open(sessionfile,"w").close()

    else: # anything else
        commands.append(lambda:logger.warning(strings.LOGGER_SESSION_NOFILE))

        # clear both files
        open(logfile,"w").close()
        open(sessionfile,"w").close()

    logger=DMXLogger(sessionFile=sessionfile,logFile=logfile) # generate the logger

    for command in commands: command()

    logger.info(strings.LOGGER_INITIALISED)

    return logger
