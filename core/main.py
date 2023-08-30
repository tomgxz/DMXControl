if __name__ == "__main__":
    from ..utils.exceptions import ModuleRunError
    raise ModuleRunError()

def initialise(argv=None):

    if len(argv) < 2:
        raise IndexError(
            "Not enough arguments given to run the program. Run python run.py help for more information"
        )
    
    if argv[1] in ["help","h","-help","-h"]:

        print("""
COMMANDS:

    help:
        aliases: h, -help, -h
        desc: outputs this page
        args: None

    dmxcontrol:
        aliases: None
        desc: initalizes the DMXControl module
        args: 
            
            -nogui:
                aliases: -ng
                desc: Prevents the GUI from being initialized
            
            -logtoconsole:
                aliases: -log, -l
                desc: Enables DMXLogger.loggingStdoutHandler from outputting to the console from level logger.LOG, as opposed to logger.ERROR """)

    if argv[1] == "dmxcontrol":

        from .DMXControl import DMXControl

        createGUI = True
        logToConsole = False

        if "-nogui" in argv[1:] or "-ng" in argv[1:]: createGUI = False
        if "-logtoconsole" in argv[1:] or "-log" in argv[1:] or "-l" in argv[1:]: logToConsole = True

        DMXControl(createGUI,logToConsole)