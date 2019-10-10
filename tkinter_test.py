import tkinter as tk

class Application( tk.Frame ):
    def __init__( self, master=None):
        super().__init__(master)
        self.master = master
        self.draw = False
        self.pack()
        self.create_widgets()
        self.create_canvas()

    def callback( self, event ):
        if self.draw:
            print( 'Stopping drawing!' )
            self.draw = False
        else:
            print( 'You can draw now!' )
            self.draw = True

    def mmove( self, event ):
        if self.draw:
            print( event.x, event.y )

    def create_canvas( self ):
        w = tk.Canvas( self.master, width = 200, height = 100 )
        w.bind( '<Button-1>', self.callback )

        w.bind( '<Motion>', self.mmove )

        w.pack()

        w.create_line(0, 0, 200, 100)
        w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

        w.create_rectangle(50, 25, 150, 75, fill="blue")


    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.listbox = tk.Listbox( self, listvariable = 'a b c' )
        self.listbox.pack( side = 'right' )

    def say_hi(self):
        print("hi there, everyone!")



root = tk.Tk()
app = Application( master = root )
app.mainloop()