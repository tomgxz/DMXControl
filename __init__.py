import numpy as np

import data.default_settings as settings
from utils.interface import DMXInterface
from utils.logger import initialize_logger

class DMXControl():
    
    def __init__(self):
        self.logger = initialize_logger(settings.LOGGER_SESSION_FILE,settings.LOGGER_LOG_FILE)

        self.FORMAT = settings.COLOR_FORMAT
        self.PIXELCOUNT = settings.PIXEL_COUNT
        self.FADEAMT = settings.FADE_FACTOR

        self.DIMMED = settings.DIMMED
        self.MONO = settings.COLOR_MONO

        self.DMXVALUES = len(self.FORMAT)*self.PIXELCOUNT
        self.BLACK = np.array([[0 for __ in range(len(self.FORMAT))] for _ in range(self.PIXELCOUNT)])

        self.previouscontent = self.BLACK

        self.interface = DMXInterface(self.logger)

        self.startScreenCap()


    def startScreenCap(self):
        import utils.effects.screencap as screencap
        
        previousOutput = None
        previousOutputDimensions = None

        while True:

            output, previousOutput, previousOutputDimensions = screencap.screencap(
                previousOutput=previousOutput,
                previousOutputDimensions=previousOutputDimensions,
                pixelcount=16
            )

            universeoutput = []

            for pixel in output:
                for sub in pixel:
                    universeoutput.append(sub)

            self.interface.send_universe(universeoutput)


DMXControl()
