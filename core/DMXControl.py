if __name__ == "__main__":
    from ..utils.exceptions import ModuleRunError
    raise ModuleRunError()

import numpy as np
import threading

import data.default_settings as default_settings
from utils.interface import DMXInterface
from utils.logger import initialize_logger, DMXLogger
from utils.settingshandler import DMXSettingsHandler
from utils.threadhandler import DMXThreadHandler
from utils.userinterface import DMXUserInterface

class DMXControl():
    """ Initializes the DMXControl application. """
    
    def __init__(self,createGUI=True,logToConsole=False) -> None:
        """ Constructs a :class: `DMXControl <DMXControl>` """
        
        self.logger:DMXLogger = initialize_logger(default_settings.LOGGER_SESSION_FILE,default_settings.LOGGER_LOG_FILE,logToConsole=logToConsole)
        self.settings = DMXSettingsHandler()
        self.threadhandler = DMXThreadHandler()

        self.FORMAT = default_settings.COLOR_FORMAT
        self.PIXELCOUNT = self.settings.pixel_count

        self.DMXVALUES = len(self.FORMAT)*self.PIXELCOUNT
        self.BLACK = np.array([[0 for __ in range(len(self.FORMAT))] for _ in range(self.PIXELCOUNT)])

        self.previouscontent = self.BLACK

        self.interface = DMXInterface(self.logger)

        t = threading.Thread(target=self.startScreenCap,args=[])
        self.threadhandler.append(t)
        t.start()

        if createGUI:

            self.ui = DMXUserInterface(self.logger,self.settings)
            self.ui.root.mainloop()

    def startScreenCap(self) -> None:
        """ Start the screencapture effect from `utils.effects.screeencap` and output via `DMXInterface` """

        import utils.effects.screencap as screencap
        
        previousOutput:np.ndarray = None
        previousOutputDimensions:tuple[int] = None

        while True:

            if self.settings.kill_output:

                clear_universe:list[int] = [0 for _ in range(512)]
                self.interface.send_universe(clear_universe)

                break


            output, previousOutput, previousOutputDimensions = screencap.screencap(
                previousOutput=previousOutput,
                previousOutputDimensions=previousOutputDimensions,
                pixelcount=self.settings.pixel_count,
                pixelreduce=self.settings.pixel_reduce,
                pixelcolorformat=self.FORMAT,
                fadefactor=self.settings.fade_factor,
                colorenhancement=self.settings.color_enhance,
                colordimming=self.settings.global_dimming
            )

            universeoutput:list[int] = []

            for pixel in output:
                for sub in pixel:
                    universeoutput.append(sub)

            self.interface.send_universe(universeoutput)
