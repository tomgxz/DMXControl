from dmx import DMX
import numpy as np
import math,time
from mss import mss
from PIL import Image,ImageEnhance
from serial import SerialException

import utils.settings as settings
from utils.logger import initialize_logger
from utils.interface import DMXInterface

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

    def connect(self):
        self.interface = DMX(num_of_channels=self.DMXVALUES)
        self.screencapture = mss()

    def update(self):
        #print("UPDATE")

        sct_img = self.screencapture.grab({"top":270,"left":480,"width":960,"height":540})

        img = Image.frombytes("RGB",(sct_img.width,sct_img.height),sct_img.rgb)
        img = ImageEnhance.Color(img).enhance(2)
        img = img.resize((1 if self.MONO else 16,1),Image.ANTIALIAS)

        img = np.array(img)[0]

        i=1

        if not self.MONO: # if mono is false
            for pixel in img: # for pixel in image (where the image is 1 pixel high and a np.array)
                for sub in pixel: # for part (of [r,g,b]) in pixel

                    # get the previous content of this pixel
                    prev = self.previouscontent[math.floor((i-1)/3)][(i-1)%3]

                    # if the previous content was a lower value
                    if int(prev)-int(sub) <= -self.FADEAMT: 
                        sub = prev + self.FADEAMT

                    # if the previous content was a higher value
                    if int(prev)-int(sub) >= self.FADEAMT: 
                        sub = prev - self.FADEAMT

                    # clamp the new value between 0 and 255
                    sub = max(min(sub, 255),0)

                    # format the dmx value
                    msub = int(self.colorfunction(sub)*(0.6 if (i-1)%3 == 2 else 1))

                    # set the value of the pixel in question, but dont send to the interface
                    self.interface.set_data(i,msub,auto_send=False)

                    # set the value of the pixel in the image array so that it can be stored for self.previouscontent
                    img[math.floor((i-1)/3)][(i-1)%3] = sub
                    i+=1

                    if i > self.DMXVALUES: break
                if i > self.DMXVALUES: break

        else: # if the image is mono

            pass

        # store in previous content for fade functions
        self.previouscontent = img

        # send the dmx content through the interface
        self.interface.send()
    
    def colorfunction(self,x:int) -> int:
        return ((x/510)**2)*1020*self.DIMMED

DMXControl()
