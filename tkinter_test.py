import tkinter as tk
from lxml.etree import *

class Application( tk.Frame ):
    def __init__( self, master = None ):
        super().__init__( master )
        self.master = master
        self.draw = False
        self.pack()
        self.create_widgets()

    def callback( self, event ):
        x = event.x
        y = event.y
        d = 10
        o = {'x1': x - d, 'y1': y - d, 'x2': x + d, 'y2': y + d }

        z = self.canvas.find_overlapping( **o )
        items = self.canvas.find_overlapping( **o )

        res = {'x': [], 'y': []}
        cellboundaries = []
        for item in items:

            itemtags = self.canvas.gettags( item )

            if 'coordinates' not in itemtags:
                continue

            cellboundaries.append( int( itemtags[1][:-2] ))
            
            # print( item )
            coords = self.canvas.coords( item )
            # print( coords )

            if coords[0] != 0:
                res['x'].append( coords[0] )

            else:
                res['y'].append( coords[-1] )

        cellboundaries.sort()
        res['x'].sort()
        res['y'].sort()

        if len( res['x'] ) == 1:
            res['x'] = [0] + res['x']

        cx = cellboundaries[2]
        cy = cellboundaries[0]

        cell = self.canvas.find_closest( x, y )


        print( self.canvas.gettags( cell ))
        print( 'sdfsdfsdf' )

        self.canvas.addtag_closest( 'WoodWall', x, y )
        self.canvas.create_rectangle( res['x'][0],res['y'][0], res['x'][1], 
            res['y'][1], fill = 'red', 
            tags = tag )

        # self.draw = True

    def mmove( self, event ):
        if self.draw:
            print( event.x, event.y )

    
    def process_canvas( self ):

        meat = []
        
        for item in self.canvas.find_all():
            if 'coordinates' in self.canvas.gettags( item ):
                continue
        
            meat.append( item )


        height = 25
        width = 80
        maproot = Element( 'Map', {'Height': str( height ), 'Width': str( width )})
        maproot.text = '\n\t'
        for x in range( width ):
            for y in range( height ):
                
                e = SubElement( maproot, 'cell', {'X': str( x ), 'Y': str( y )} )
                e.text = '\n\t\t'
                e.tail = '\n\t'
        with open( 'test.xml', 'w' ) as f:
            f.write( tostring( maproot ).decode( 'utf-8' ))
        for chunk in meat:
            tags = self.canvas.gettags( chunk )
            coords = self.canvas.coords( chunk )
            x = str( int( coords[0] ) // 10 )
            y = str( int( coords[1] ) // 10 )
            print( x, y )
            # x = tags[0].split( ',' )[0].split( '-' )[-1]
            # y = tags[0].split( ',' )[1].split( '-' )[-1]
            e = maproot.find( './/cell[@X="{0}"][@Y="{1}"]'.format( x, y ))

            for tag in tags:
                se = SubElement( e, 'object', {'Name': tag} )

                se.tail = '\n\t\t\t'
        #e[-1].tail = e.tail

        #maproot[-1].tail = '\n'

        print( tostring( maproot ).decode( 'utf-8' ))        

    def create_widgets( self ):
        self.process = tk.Button( self )
        self.process['text'] = 'Process'
        self.process['command'] = self.process_canvas
        self.process.pack( side = 'right' )

        canvaswidth = 800
        canvasheight = 250

        self.cframe = tk.Frame( self.master )
        self.cframe.pack( side = tk.LEFT )
        self.canvas = tk.Canvas( self.cframe, width = canvaswidth, height = canvasheight, 
            relief = tk.GROOVE, bg = 'white' )
        self.canvas.bind( '<Button-1>', self.callback )

        self.canvas.bind( '<Motion>', self.mmove )

        self.canvas.pack()

        for w in range( 0, canvaswidth + 10, 10 ):
            self.canvas.create_line( w, 0, w, canvasheight, tags = ('coordinates',w/10) )
        
        for h in range( 0, canvasheight + 10, 10 ):
            self.canvas.create_line( 0, h, canvaswidth, h, tags = ('coordinates', h/10) )

        for w in range( 0, canvaswidth, 10 ):
            for h in range( 0, canvasheight, 10 ):
                self.canvas.create_rectangle( w, h, w + 10, h + 10, fill = 'green' )

        self.mframe = tk.Frame( self.master )
        self.mframe.pack( side = tk.RIGHT )

        self.listbox = tk.Listbox( self.mframe )
        for i in range( 10 ):
            self.listbox.insert( i, 'test - ' + str( i ))
        self.listbox.pack( side = tk.TOP )


        self.quit = tk.Button( self.mframe, text="QUIT", fg="red", 
            command = self.master.destroy )

        self.quit.pack( side= tk.BOTTOM )




    def say_hi(self):
        print("hi there, everyone!")



root = tk.Tk()
root.geometry( '1000x250' )
app = Application( master = root )
app.mainloop()

