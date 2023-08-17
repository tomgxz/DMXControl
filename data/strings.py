if __name__ == "__main__":
    from ..utils.exceptions import ModuleRunError
    raise ModuleRunError()

PROJECT_NAME = "DMX Controller"
PROJECT_DESC = "Python-based DMX interface controller, primarily used for emulating monitor displays."
PROJECT_AUTHOR = "Tom_gxz"

GENERIC_INVALID_ARGUMENT = "Invalid argument: {}"
GENERIC_MODULE_RUN_ERROR = "This module is to be used in conjunction with the DMXControl application and not as a standalone module."

INTERFACE_ABORT_CONNECTION = "Could not connect to RS-485 DMX Interface."
INTERFACE_ABORT_CONNECTION_DETAIL = "Could not connect to RS-485 DMX Interface after {} attempts, aborting..."
INTERFACE_CONNECTED = "Connected to RS-485 DMX Interface."
INTERFACE_DISCONNECTED = "RS-485 DMX Interface disconnected."
INTERFACE_FAILED_CONNECTION = "Could not connect to RS-485 DMX Interface."
INTERFACE_FAILED_CONNECTION_DETAIL = "Could not connect to RS-485 DMX Interface, retrying in {}... "
INTERFACE_NOT_CONNECTED = "Interface must be connected to send data."

INTERFACE_UNIVERSE_MAX512 = "Universe must not exceed 512 entries"
INTERFACE_UNIVERSE_MUSTBELIST = "Universe data must be contained in a list structure."
INTERFACE_UNIVERSE_MUSTHAVEDATA = "Universe must contain data"

INTERFACE_CHANNEL_ADDRESSMUSTBEINT = "Channel address must be an integer"
INTERFACE_CHANNEL_ADDRESSCONSTRAINT = "Channel address must be between 1 and 512"
INTERFACE_CHANNEL_CONTENTMUSTBEINT = "Channel content must be an integer"
INTERFACE_CHANNEL_CONTENTCONSTRAINT = "Channel content must be between 0 and 255"

LOGGER_EXCEPTIONHANDLINGERROR = "An exception occured during the handling of another Logger exception."
LOGGER_FILENOTFOUND = "Logging {} file not found at URL: {}"
LOGGER_INITIALISED = "Logging initialised"
LOGGER_PREVLOG_NOFILE = "Previous log file does not exist"
LOGGER_SESSION_NOFILE = "Session file does not exist"
LOGGER_SESSION_EMPTY = "Session file is empty"
LOGGER_SESSION_NODATE = "No date created attribute in session file - previous log file will be deleted"

UI_APPLICATION_CLOSED = "Application closed, terminating program..."

UI_TITLE_WINDOW = "DMX Controller"
UI_TITLE_CONTENT = "DMX Controller"

UI_OPTION_GLOBALDIMMING_LABEL = "Global Dimming"
UI_OPTION_PIXELCOUNT_LABEL = "Pixel Count"
UI_OPTION_PIXELREDUCE_LABEL = "Pixel Reduce"
UI_OPTION_COLORENHANCE_LABEL = "Color Enhance"