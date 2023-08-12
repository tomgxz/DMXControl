from dmx import DMX
from serial import SerialException
import time

from utils.exceptions import InterfaceFailedConnectionException,InterfaceInvalidArgumentException,InterfaceNotConnectedException,InterfaceDisconnectedException
import utils.settings as settings

class DMXInterface():
    
    def __init__(self):

        self.connected = False
        self.__connection_timeout = settings.INTERFACE_CONNECTION_TIMEOUT
        self.__connection_attempts = 0
        self.__connection_delay = settings.INTERFACE_CONNECTION_DELAY
        
        while not self.connected and self.__connection_timeout > self.__connection_attempts:

            if self.__attempt_connection():
                self.connected = True
                self.__connection_attempts = 0

            else:
                self.__connection_attempts += 1
                time.sleep(self.__connection_delay/1000)

    def __attempt_connection(self):
        try: 
            self.connect()
            return True
        except InterfaceFailedConnectionException as exec:
            return False
     
    def connect(self):
        try: self.interface = DMX(num_of_channels=512)
        except Exception as exec:
            print(type(exec))
            raise InterfaceFailedConnectionException()
           
    def __send_universe(self,data:list):
        for datum in enumerate(data):
            self.interface.set_data(datum[0],datum[1],auto_send=False)

        try: self.interface.send()
        except SerialException: raise InterfaceDisconnectedException()

    def __send_channel(self,channel_address:int,channel_content:int,auto_send=True):
        try: self.interface.set_data(channel_address,channel_content,auto_send=auto_send)
        except SerialException as exec: raise InterfaceDisconnectedException()
