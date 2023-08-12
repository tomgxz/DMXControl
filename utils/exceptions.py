class ModuleRunError(Exception):
    def __init__(self):
        super().__init__("This module is to be used in conjunction with the DMXControl application and not as a standalone module.")

if __name__ == "__main__":
    raise ModuleRunError()
