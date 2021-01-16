import tkinter as tk
from . import zooming
from .import themes

class Canvas( tk.Frame ):
    def __init__( self, parent,w_diff, h_diff, oom ):

        width = 80 * w_diff
        height = 25 * h_diff

        self.canvas = zooming.Zoom_Canvas( 
            master = parent, #self.contentframe, 
            oom = oom, 
            width = width, 
            height = height, 
            background = themes.canvas_bg, 
            highlightthickness = 0
        )

        self.canvas.grid( column = 1, row = 1, sticky = tk.N )

        for w in range( w_diff//2, width, w_diff ):
            for h in range( h_diff//2, height, h_diff ):
                # bbox = (w + w_diff/3, h + h_diff/3, w + 2*w_diff/3, h + 2*h_diff/3)
                self.canvas.create( 
                    shape = 'circle', 
                    center = (w, h), 
                    radius = 2, 
                    fill = themes.canvas_fill, 
                    tags = 'dot', 
                    outline = themes.canvas_bg
                )

