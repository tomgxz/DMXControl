if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from dmx import DMX
from serial import SerialException
from datetime import timedelta as datetime_timedelta
from humanize import naturaldelta as humanize_naturaldelta
import time

import utils.settings as settings
from utils.exceptions import InterfaceFailedConnectionException,InterfaceInvalidArgumentException,InterfaceNotConnectedException,InterfaceDisconnectedException,InterfaceAbortConnectionException
from utils.logger import Logger as DMXLogger

class DMXInterface():
    
    def __init__(self,logger:DMXLogger):
        assert type(logger) == DMXLogger

        self.connected = False
        self.__connection_timeout = settings.INTERFACE_CONNECTION_TIMEOUT
        self.__connection_attempts = 0
        self.__connection_delay = settings.INTERFACE_CONNECTION_DELAY

        self.__connection_attempt_validation = lambda: self.__connection_timeout > self.__connection_attempts
        if self.__connection_timeout == -1: self.__connection_attempt_validation = lambda: True
        
        while not self.connected and self.__connection_attempt_validation():

            if self.__attempt_connection():
                self.connected = True
                self.__connection_attempts = 0

            else:
                self.__connection_attempts += 1

                if not self.__connection_attempt_validation():
                    logger.exception(f"Could not connect to RS-485 DMX Interface after {self.__connection_attempts} attempts, aborting...")
                    raise InterfaceAbortConnectionException()
                else:
                    logger.warning(f"Could not connect to RS-485 DMX Interface, retrying in {humanize_naturaldelta(datetime_timedelta(milliseconds=self.__connection_delay))}... ")

                time.sleep(self.__connection_delay/1000)

    def __attempt_connection(self):
        try: 
            self.connect()
            return True
        except InterfaceFailedConnectionException as exec:
            return False
     
    def connect(self):
        try: self.interface = DMX(num_of_channels=512)
        except ConnectionError as exec:
            raise InterfaceFailedConnectionException()
           
    def __send_universe(self,data:list):
        try: assert type(data) == list
        except AssertionError: 
            raise InterfaceInvalidArgumentException(
                "Universe data must be contained in a list structure.")
        
        try: assert data not in [[],None]
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Universe must contain data")
        
        try: assert len(data) <= 512
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Universe must not exceed 512 entries")

        try: assert self.connected == True
        except AssertionError:
            raise InterfaceNotConnectedException()

        for datum in enumerate(data):
            self.interface.set_data(datum[0],datum[1],auto_send=False)

        try: self.interface.send()
        except SerialException: raise InterfaceDisconnectedException()

    def __send_channel(self,channel_address:int,channel_content:int,auto_send=True):
        try: assert type(channel_address) == int
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Channel address must be an integer")
        
        try: assert type(channel_content) == int
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Channel content must be an integer")
        
        try: assert channel_address > 0 and channel_address <= 512
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Channel address must be between 1 and 512")
        
        try: assert channel_content >=0 and channel_content <= 255
        except AssertionError:
            raise InterfaceInvalidArgumentException(
                "Channel content must be between 0 and 255")

        try: assert self.connected == True
        except AssertionError:
            raise InterfaceNotConnectedException()

        try: self.interface.set_data(channel_address,channel_content,auto_send=auto_send)
        except SerialException as exec: raise InterfaceDisconnectedException()
