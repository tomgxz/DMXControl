if __name__ == "__main__":
    from exceptions import ModuleRunError
    raise ModuleRunError()

from tkinter import Tk,Label,Frame,Scale
from tkinter.font import Font

from utils.logger import Logger
from utils.settingshandler import DMXSettingsHandler

class DMXUserInterface():
    def __init__(self,logger:Logger,settingshandler:DMXSettingsHandler):

        assert type(logger) == Logger
        assert type(settingshandler) == DMXSettingsHandler

        self.__logger = logger
        self.__settings = settingshandler

        self.__initialize_tk()

        self.__main_screen()

        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.__tk_on_close)

    def __initialize_tk(self):
        self.root = Tk()
        
        self.__colors = {
            
            "light":"#fdfdfd",
            "white":"#ffffff",

            "dark":"#0c0200",

            "danger":"#EA5D5C",
            "warning":"#ffc107",
            "success":"#4dbd74",

            "primary": {
                "light": "#bc8abf",
                "normal": "#9f58a4",
                "dark": "#6f3e73"
            },

            "secondary": {
                "light": "#9d8cbf",
                "normal": "#735aa3",
                "dark": "#513f72"
            },

            "info": {
                "light": "#90c9ea",
                "normal": "#60b2e1",
                "dark": "#437d9e"
            },

            "success":"#31ac74",
            "warning":"#ddd02e",
            "danger":"#e93a19"
        }
        
        self.__font_primary = "Poppins"
        self.__font_secondary = "Lato"

        self.__title_font=Font(
            family=self.__font_primary,
            size="36",
            weight="bold"
        )

        self.__header_font=Font(
            family=self.__font_secondary,
            size="24",
        )

        self.__caption_font=Font(
            family=self.__font_primary,
            size="20",
            weight="bold"
        )

        self.__body_font=Font(
            family=self.__font_primary,
            size="12"
        )

        self.__bgcolor=self.__colors["light"]

        self.root.title("DMX Controller")
        self.__window_width = 960
        self.__window_height = 540
        self.root.geometry(f"{self.__window_width}x{self.__window_height}")
        self.root.minsize(self.__window_width,self.__window_height)
        #self.root.state("zoomed")

        #self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.configure(bg=self.__bgcolor)


    def __tk_on_close(self):
        self.root.destroy()
        self.__settings.enable_kill_output()
        self.__logger.info("Application closed, terminating program...")
        
    def __main_screen(self):
        title = self.__tk_create_title()

        main = Frame(self.root,bg=self.__bgcolor)
        main.pack()

        display = Frame(main,bg=self.__bgcolor)
        display.grid(row=0,column=0)

        options = Frame(main,bg=self.__bgcolor)
        options.grid(row=0,column=1)

        optionstitle = Label(options,bg=self.__bgcolor,text="Options",font=self.__header_font,width=options.size()[1])
        optionstitle.grid(row=0,column=0)


        # Global Dimming
        #region

        optionframe_globaldimming = Frame(options,bg=self.__bgcolor)
        optionframe_globaldimming.grid(row=1,column=0)

        optionlabel_globaldimming = Label(optionframe_globaldimming,bg=self.__bgcolor,text="Global Dimming")
        optionlabel_globaldimming.pack(side="left")

        optionslider_globaldimming = Scale(optionframe_globaldimming,bg=self.__bgcolor,borderwidth=0,from_=0,to=1,orient="horizontal",resolution=0.01)
        optionslider_globaldimming.set(1)
        optionslider_globaldimming.pack(side="right")

        optionslider_globaldimming.bind("<ButtonRelease-1>",lambda e: self.__settings.set_global_dimming(optionslider_globaldimming.get()))

        #endregion

        # Pixel Count
        #region

        optionframe_pixelcount = Frame(options,bg=self.__bgcolor)
        optionframe_pixelcount.grid(row=2,column=0)

        optionlabel_pixelcount = Label(optionframe_pixelcount,bg=self.__bgcolor,text="Pixel Count")
        optionlabel_pixelcount.pack(side="left")

        optionslider_pixelcount = Scale(optionframe_pixelcount,bg=self.__bgcolor,borderwidth=0,from_=1,to=16,orient="horizontal",resolution=1)
        optionslider_pixelcount.set(16)
        optionslider_pixelcount.pack(side="right")

        optionslider_pixelcount.bind("<ButtonRelease-1>",lambda e: self.__settings.set_pixel_count(optionslider_pixelcount.get()))

        #endregion

        # Pixel Reduce
        #region

        optionframe_pixelreduce = Frame(options,bg=self.__bgcolor)
        optionframe_pixelreduce.grid(row=3,column=0)

        optionlabel_pixelreduce = Label(optionframe_pixelreduce,bg=self.__bgcolor,text="Pixel Reduce")
        optionlabel_pixelreduce.pack(side="left")

        optionslider_pixelreduce = Scale(optionframe_pixelreduce,bg=self.__bgcolor,borderwidth=0,from_=1,to=16,orient="horizontal",resolution=1)
        optionslider_pixelreduce.set(1)
        optionslider_pixelreduce.pack(side="right")

        optionslider_pixelreduce.bind("<ButtonRelease-1>",lambda e: self.__settings.set_pixel_reduce(optionslider_pixelreduce.get()))

        #endregion
        
        # Color Enhance
        #region

        optionframe_colorenhance = Frame(options,bg=self.__bgcolor)
        optionframe_colorenhance.grid(row=4,column=0)

        optionlabel_colorenhance = Label(optionframe_colorenhance,bg=self.__bgcolor,text="Color Enhance")
        optionlabel_colorenhance.pack(side="left")

        optionslider_colorenhance = Scale(optionframe_colorenhance,bg=self.__bgcolor,borderwidth=0,from_=1,to=5,orient="horizontal",resolution=0.1)
        optionslider_colorenhance.set(2)
        optionslider_colorenhance.pack(side="right")

        optionslider_colorenhance.bind("<ButtonRelease-1>",lambda e: self.__settings.set_color_enhance(optionslider_colorenhance.get()))

        #endregion

        """
        
        # NAME
        #region

        optionframe_ = Frame(options,bg=self.bgcolor)
        optionframe_.grid(row=1,column=0)

        optionlabel_ = Label(optionframe_,bg=self.bgcolor,text="Global Dimming")
        optionlabel_.pack(side="left")

        optionslider_ = Scale(optionframe_,bg=self.bgcolor,borderwidth=0,from_=0,to=1,orient="horizontal",resolution=0.01)
        optionslider_.set(1)
        optionslider_.pack(side="right")

        optionslider_.bind("<ButtonRelease-1>",lambda e: self.settings.set_global_dimming(optionslider_.get()))

        #endregion
        
        """

    def __tk_create_title(self):
        title=Label(self.root,text="DMX Controller",font=self.__title_font,fg=self.__colors["primary"]["normal"],bg=self.__bgcolor)
        title.pack()
        return title