import tkinter as tk
from lxml.etree import *
from PIL import Image, ImageTk
import time

class Application( tk.Frame ):
    def __init__( self, master = None, oom = 10 ):
        super().__init__( master )
        self.master = master
        self.draw = False
        self.pack()
        self.oom = oom
        self.recentchanges = []
        self.currenttime = 0
        self.currenttimetag = None
        self.drawing = False
        self.color = None
        self.create_widgets()

    def setcolor( self ):
        selection = self.listbox.curselection()

        if selection == ():
            return
        
        color = mapping[ self.listbox.get( selection[0] )]
        self.color = color


    def stopdrawing( self, event ):
        self.drawing = False

    def callback( self, event ):
        x = event.x
        y = event.y
        d = self.oom
        o = {'x1': x - d, 'y1': y - d, 'x2': x + d, 'y2': y + d }

        if self.drawing == False:
            self.currenttimetag = time.time()
            self.recentchanges.append( self.currenttimetag )
            self.drawing = True

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

        selection = self.listbox.curselection()

        if selection == ():
            return

        tag = self.listbox.get( selection[0] )

        self.setcolor()

        # print( tag )
        newid = self.canvas.create_rectangle( res['x'][0],res['y'][0], res['x'][1], 
            res['y'][1], fill = self.color, 
            tags = ( tag, 'item', self.currenttimetag) )



        
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
            x = str( int( coords[0] ) // self.oom )
            y = str( int( coords[1] ) // self.oom )

            # x = tags[0].split( ',' )[0].split( '-' )[-1]
            # y = tags[0].split( ',' )[1].split( '-' )[-1]
            e = maproot.find( './/cell[@X="{0}"][@Y="{1}"]'.format( x, y ))

            for tag in tags:
                se = SubElement( e, 'object', {'Name': tag} )

                se.tail = '\n\t\t\t'
        #e[-1].tail = e.tail

        #maproot[-1].tail = '\n'

        print( tostring( maproot ).decode( 'utf-8' ))
    
    def reset_canvas( self ):
        for item in self.canvas.find_withtag( 'item' ):
            self.canvas.delete( item )

    def undo( self ):
        print( self.recentchanges )
        if self.recentchanges != []:
            items = self.canvas.find_withtag( self.recentchanges[-1])
            for item in items:
                self.canvas.delete( item )
            self.recentchanges = self.recentchanges[:-1]



    def create_widgets( self ):
        self.process = tk.Button( self, text = 'Process', command = self.process_canvas )
        self.process.pack( side = tk.RIGHT )

        self.process = tk.Button( self, text = 'reset', command = self.reset_canvas )
        self.process.pack( side = tk.RIGHT )

        self.process = tk.Button( self, text = 'undo', command = self.undo )
        self.process.pack( side = tk.RIGHT )

        canvaswidth = 80 * self.oom
        canvasheight = 25 * self.oom

        self.cframe = tk.Frame( self.master )
        self.cframe.pack( side = tk.LEFT )
        self.canvas = tk.Canvas( self.cframe, width = canvaswidth, height = canvasheight, 
            relief = tk.GROOVE, bg = 'white' )
        self.canvas.bind( '<ButtonRelease-1>', self.stopdrawing )
        self.canvas.bind( '<Button-1>', self.callback )
        self.canvas.bind( '<B1-Motion>', self.callback )
        self.canvas.pack()

        for w in range( 0, canvaswidth + self.oom, self.oom ):
            self.canvas.create_line( w, 0, w, canvasheight, tags = ('coordinates',w / self.oom ))
        
        for h in range( 0, canvasheight + self.oom, self.oom ):
            self.canvas.create_line( 0, h, canvaswidth, h, tags = ('coordinates', h / self.oom ))

        for w in range( 0, canvaswidth, self.oom ):
            for h in range( 0, canvasheight, self.oom ):
                self.canvas.create_rectangle( w, h, w + self.oom, h + self.oom, fill = 'green', tags = 'base' )

        img = Image.open( r'test.bmp' )
        iw, ih = img.size
        ratio = self.oom / ih
        img = img.resize( (int( iw * ratio ), self.oom ) )
        print( img.size, ratio, ih )
        self.img = img = ImageTk.PhotoImage( img )
        self.canvas.create_image( (0, 0), image = img, anchor = 'nw' )

        self.mframe = tk.Frame( self.master )
        self.mframe.pack( side = tk.LEFT )

        self.listbox = tk.Listbox( self.mframe )
        for i in range( 4 ):
            self.listbox.insert( i, 'WoodWall' + str( i ))
        self.listbox.pack( side = tk.TOP )


        # self.quit = tk.Button( self.mframe, text="QUIT", fg="red", 
        #     command = self.master.destroy )

        # self.quit.pack( side= tk.BOTTOM )

        # self.bframe = tk.Frame( self.master )
        # self.bframe.pack( side = tk.BOTTOM )

        self.infobox = tk.Listbox( self.mframe )
        self.canvas.bind( '<Button-3>', self.getinfo )

        self.infobox.pack( side = tk.BOTTOM )




    def getinfo( self, event ):
        self.infobox.delete( 0, tk.END )
        d = .1
        x = event.x
        y = event.y
        o = {'x1': x - d, 'y1': y - d, 'x2': x + d, 'y2': y + d }
        items = self.canvas.find_overlapping( **o )

        for item in items[::-1]:
            self.infobox.insert( items.index( item ) + len( items ), self.canvas.gettags( item ))



orderofmagnitude = 30

width = 100 * orderofmagnitude
height = 30 * orderofmagnitude 

mapping = {'WoodWall' + str(i): colors[i] for i in range( len( colors ))}

root = tk.Tk()
root.geometry( str( width ) + 'x' + str( height ))
app = Application( master = root, oom = orderofmagnitude )
app.mainloop()

