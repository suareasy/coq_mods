import tkinter as tk
from . import themes

class InfoFrame( tk.Frame ):
    def __init__( self, master ):

        self.infotext = tk.Text( 
            master, 
            **themes.o, 
            wrap = tk.WORD, 
            font = ('Consolas', 13), 
            state = tk.DISABLED, height = 10
        )

        self.infotext.grid( column = 0, row = 0, sticky = tk.W )


        self.canvas2 = tk.Canvas( master, **themes.canvassettings )
        self.canvas2.grid( column = 2, row = 0 )

        self.infobox = tk.Listbox( master, **themes.o, height = 13 )
        self.infobox.grid( column = 3, row = 0, sticky = tk.E, padx = 5 )

