from mss import mss
from PIL import Image,ImageEnhance

import numpy as np

screencapture = mss()

colormap:dict[str,int] = {
    "R":1,
    "G":1,
    "B":0.6,
    "A":1,
    "W":1,
}

def clamp(i:int|float,imax:int|float=1,imin:int|float=0) -> int|float:
    return max(min(i, imax),imin)

def colorfunction(x:int,color:str="R",dimming:int=1) -> int:
    assert color in list(colormap.keys())
    return ((x/510)**2)*1020*colormap[color]*dimming

def formatvalue(
        sub:int, # r,g,b etc value
        color:str, # color type, eg r,g,b
        prev:int = -1, # previous color, optional, -1 if no previous color
        fadefactor:int = 15,
        colordimming:float = 1,
    ) -> tuple[int]:

    if prev >= 0 and fadefactor > 0:

        # if the previous content was a lower value
        if int(prev)-int(sub) <= -fadefactor: 
            sub = prev + fadefactor

        # if the previous content was a higher value
        if int(prev)-int(sub) >= fadefactor: 
            sub = prev - fadefactor
                
        # clamp the new value between 0 and 255
        sub = clamp(sub,255,0)
    
    # format the dmx value
    msub = int(colorfunction(sub,color,colordimming))

    return (sub,msub)

def screencap(
        previousOutput:np.ndarray=None,
        previousOutputDimensions:tuple[int]=(),
        pixelcount:int | list[int] = 1,
        pixelreduce:int = 1,
        pixelcolorformat:list[str] = ["R","G","B"],
        fadefactor:int = 15,
        colorenhancement:float = 2,
        colordimming:float = 1
    ) -> tuple[np.ndarray,np.ndarray,tuple[int]]:

    for color in pixelcolorformat: assert color in list(colormap.keys())

    # frequently used value given shorter name for better readability
    pcflen = len(pixelcolorformat)
    
    sct_img = screencapture.grab({"top":270,"left":480,"width":960,"height":540})  

    dimensions:tuple[int] = (1,1)
    usepixelreduce = False

    if type(pixelcount) == int:
        if pixelcount < pixelreduce:
            pixelreduce = pixelcount

        usepixelreduce = pixelreduce > 1 and pixelcount % pixelreduce == 0

        originaldimensions = (pixelcount,1)

        if usepixelreduce:
            outputpixelcount = pixelcount
            pixelcount = int(pixelcount / pixelreduce)

        dimensions = (pixelcount,1)

    elif type(pixelcount) == list[int]:
        
        if len(pixelcount) > 2 or len(pixelcount) < 1:
            raise Exception()
        
        elif len(pixelcount) == 2:
            dimensions = tuple(pixelcount)

        elif len(pixelcount) == 1:
            dimensions = (pixelcount[0],1)

    else:
        raise Exception() # abstract
    
    assert len(dimensions) == 2

    dmxvaluecount = pcflen
    for value in dimensions: dmxvaluecount *= value

    usePreviousOutput = dimensions == previousOutputDimensions

    img = Image.frombytes("RGB",(sct_img.width,sct_img.height),sct_img.rgb)
    if colorenhancement >= 0: img = ImageEnhance.Color(img).enhance(colorenhancement)

    i=0

    if not usepixelreduce: # if no pixel reduction will take place

        img = img.resize(dimensions,Image.ANTIALIAS)

        img = np.array(img)[0]
        output = img.copy()

        if dimensions[1] == 1: # if there is only one plane

            for pixel in enumerate(img): # for pixel in image (where the image is 1 pixel high and a np.array)

                for sub in enumerate(pixel[1]): # for part (of [r,g,b]) in pixel

                    color = pixelcolorformat[sub[0]]

                    prev = -1
                    if usePreviousOutput: prev = previousOutput[pixel[0]][sub[0]]

                    formatted = formatvalue(sub[1],color,prev=prev,fadefactor=fadefactor,colordimming=colordimming)

                    # set the value of the pixel in the image array so that it can be returned
                    img[pixel[0]][sub[0]] = formatted[0]

                    # set the value in the output, to be sent to the interface
                    output[pixel[0]][sub[0]] = formatted[1]

                    if i >= dmxvaluecount: break

                if i >= dmxvaluecount: break

        else:

            for plane in enumerate(img): # for plane in image (plane is each row, each horizontal layer) (where the image is >1 pixel high and a np.array)

                for pixel in enumerate(plane[1]): # for pixel in plane

                    for sub in enumerate(pixel[1]): # for part (of [r,g,b]) in pixel

                        color = pixelcolorformat[sub[0]]

                        prev = -1
                        if usePreviousOutput: prev = previousOutput[plane[0]][pixel[0]][sub[0]]

                        formatted = formatvalue(sub,color,prev=prev,fadefactor=fadefactor,colordimming=colordimming)

                        # set the value of the pixel in the image array so that it can be returned
                        img[plane[0]][pixel[0]][sub[0]] = formatted[0]

                        # set the value in the output, to be sent to the interface
                        output[plane[0]][pixel[0]][sub[0]] = formatted[1]

                        if i >= dmxvaluecount: break

                    if i >= dmxvaluecount: break

    else: # if pixel reduction will be used

        originalimg = img.resize(originaldimensions,Image.ANTIALIAS)
        img = img.resize(dimensions,Image.ANTIALIAS)

        originalimg = np.array(originalimg)[0]
        img = np.array(img)[0]

        output = originalimg.copy()

        for pixel in enumerate(img): # for pixel in image (where the image is 1 pixel high and a np.array)

            for sub in enumerate(pixel[1]): # for part (of [r,g,b]) in pixel

                color = pixelcolorformat[sub[0]]

                prev = -1
                if usePreviousOutput: prev = previousOutput[pixel[0]][sub[0]]

                formatted = formatvalue(sub[1],color,prev=prev,fadefactor=fadefactor,colordimming=colordimming)

                for i in range(pixelreduce):
                    
                    # set the value of the pixel in the image array so that it can be returned
                    originalimg[pixel[0]+i][sub[0]] = formatted[0]

                    # set the value in the output, to be sent to the interface
                    output[pixel[0]+i][sub[0]] = formatted[1]

                if i >= dmxvaluecount: break

            if i >= dmxvaluecount: break

        img = originalimg

    # return for fade functionality
    return (output,img,dimensions)
