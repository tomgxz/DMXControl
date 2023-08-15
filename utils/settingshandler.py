if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from data import default_settings

class DMXSettingsHandler():
    def __init__(self):
        
        self.__pixel_count:int = default_settings.PIXEL_COUNT
        self.__pixel_reduce:int = default_settings.PIXEL_REDUCE
        self.__fade_factor:int = default_settings.FADE_FACTOR
        self.__global_dimming:float = default_settings.GLOBAL_DIMMING
        self.__color_enhance:float = default_settings.COLOR_ENHANCE

        self.__kill_output:bool = False

    @property
    def pixel_count(self) -> int:
        return self.__pixel_count
    
    @pixel_count.setter
    def pixel_count(self,value):
        self.__pixel_count = value

    def set_pixel_count(self,value):
        self.__pixel_count = value


    @property
    def pixel_reduce(self) -> int:
        return self.__pixel_reduce
    
    @pixel_reduce.setter
    def pixel_reduce(self,value):
        self.__pixel_reduce = value
        
    def set_pixel_reduce(self,value):
        self.__pixel_reduce = value


    @property
    def fade_factor(self) -> int:
        return self.__fade_factor
    
    @fade_factor.setter
    def fade_factor(self,value):
        self.__fade_factor = value
        
    def set_fade_factor(self,value):
        self.__fade_factor = value


    @property
    def global_dimming(self) -> float:
        return self.__global_dimming
    
    @global_dimming.setter
    def global_dimming(self,value):
        self.__global_dimming = value
        
    def set_global_dimming(self,value):
        self.__global_dimming = value


    @property
    def color_enhance(self) -> float:
        return self.__color_enhance
    
    @color_enhance.setter
    def color_enhance(self,value):
        self.__color_enhance = value

    def set_color_enhance(self,value):
        self.__color_enhance = value


    @property
    def kill_output(self):
        return self.__kill_output

    def enable_kill_output(self):
        self.__kill_output = True