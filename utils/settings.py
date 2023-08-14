if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

# The amount of pixels to output to
PIXEL_COUNT = 16

# How much to reduce the output. Must be a factor of PIXEL_COUNT
# 1 means that each pixel will have a unique output
# 2 means that each pair of pixels will be the same
# if PIXEL_REDUCE == PIXEL_COUNT, only one color will be outputted to all pixels
PIXEL_REDUCE = 1

# The factor with which fade time is calculated
FADE_FACTOR = 15

# The brightness factor of the output
DIMMED = 1

# The DMX address format for each pixel
COLOR_FORMAT = ["R","G","B"]

# Whether or not the output all one color, or many colors
# Deprecated, replaced by PIXEL_REDUCE
COLOR_MONO = 0

# How much to enhance the image, 1 preserves its original state
COLOR_ENHANCE = 2

# The time (in ms) between each attempted connection to the interface
INTERFACE_CONNECTION_DELAY = 5000

# The amount of attempts at connecting to the interface (-1 to continue until connected)
INTERFACE_CONNECTION_TIMEOUT = -1

# Default file locations for the logger
LOGGER_SESSION_FILE = "data/session.txt"
LOGGER_LOG_FILE =  "data/log/latest.log"