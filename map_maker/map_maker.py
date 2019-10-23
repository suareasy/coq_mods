import tkinter as tk
from tkinter import ttk
from lxml.etree import *
from PIL import Image, ImageTk
import time, importlib, re
import functools, operator, sys
import zooming

class Application( tk.Frame ):
    def __init__( self, master = None, oom = 10 ):
        super().__init__( master )
        self.master = master
        self.draw = False
        self.oom = oom
        self.recentchanges = []
        self.currenttime = 0
        self.currenttimetag = None
        self.currentitem = None
        self.drawing = False
        self.color = None
        self.image = None
        self.blueprints = None
        self.images = {}
        self.framebgcolor = '#525252'
        self.canvasbackground = '#141313'
        self.currentlocation = None

    def setimage( self ):

        name = self.get_tree_selection()

        if name is None:
            return

        qudobject = self.blueprints[name]


        if qudobject is not None:
            image = qudobject.tile

        if image is not None:
            image = image.image

        tags = ('object=' + name, 'item', self.currenttimetag )
        print( self.currentlocation )
        items = self.canvas.find_overlapping( **self.currentlocation )
        item =  list( filter( lambda m: 'dot' in self.canvas.gettags( m ), items ))[0]

        self.canvas.itemconfig( item, fill = self.canvas['background'], tags = ('dot', self.currenttimetag) )


        if image is not None:
            print( type( image ))

            newid = self.canvas.create( shape = 'image', 
                position = (self.currentlocation['x1'], self.currentlocation['y1']), 
                image = image, anchor = tk.NW, tags = tags )

        else:

            color = 'yellow'

            coords = [y for x,y in self.currentlocation.items()]
            coords = [x + self.oom/3 for x in coords[:2]] + [x - self.oom/3 for x in coords[2:]]
            newid = self.canvas.create( shape = 'rectangle', bbox = coords, fill = color, tags = tags )

        


    def stopdrawing( self, event ):
        self.drawing = False

    def callback( self, event ):
        x = event.x
        y = event.y
        xbar = ( x // self.oom ) * self.oom
        ybar = ( y // self.oom ) * self.oom
        o = {'x1': xbar, 'y1': ybar, 'x2': xbar + self.oom, 'y2': ybar + self.oom }

        if self.drawing == False:
            self.currenttimetag = time.time()
            self.recentchanges.append( self.currenttimetag )
            self.drawing = True


        if event.type == '6':
            if self.currentlocation == o:
                    return
            else:
                self.currentlocation = o


        else:
            self.currentlocation = o

        self.setimage()




        
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

            e = maproot.find( './/cell[@X="{0}"][@Y="{1}"]'.format( x, y ))

            regex = re.compile( r'^object=(.*)$' )
            name = list( filter( regex.match, tags ))#[0].split( '=' )[1]
            if name == []:
                continue

            name = name[0].split( '=' )[1]
            se = SubElement( e, 'object', {'Name': name} )

            se.tail = '\n\t\t\t'
        #e[-1].tail = e.tail

        #maproot[-1].tail = '\n'

        # print( tostring( maproot ).decode( 'utf-8' ))
        with open( 'map1.rpm', 'w' ) as f:
            f.write( tostring( maproot ).decode( 'utf-8' ))


    def reset_canvas( self ):
        for item in self.canvas.find_withtag( 'item' ):
            self.canvas.delete( item )

    def undo( self ):
        if self.recentchanges != []:
            items = self.canvas.find_withtag( self.recentchanges[-1])
            for item in items:
                self.canvas.delete( item )
            self.recentchanges = self.recentchanges[:-1]

    def get_tree_selection( self ):
        selection = self.tree.selection()

        if selection == () or selection is None:
            return

        else:
            self.currentitem = self.tree.item( selection[0] )['text']
            return self.currentitem


    def get_object_description( self, event ):
        name = self.get_tree_selection()

        if name is None:
            return


        object = self.blueprints.get( name )
        text = object.desc

        if text == 'None' or text is None:
            text = 'Sorry. There is no description for \'{}\''.format( name )

        self.infotext.config( state = tk.NORMAL )
        self.infotext.delete( '1.0', tk.END )
        self.infotext.insert( tk.END, text )

        self.infotext.config( state = tk.DISABLED )
        


    def create_menu_widgets( self ):

        o = {
            'background': '#333333',
            'foreground': '#c78626',
            'relief': tk.FLAT,
            'highlightthickness': 0,
            'borderwidth': 0
        }

        ttk.Style().configure( 'TFrame', background = self.framebgcolor, 
            borderwidth = 0, relief = tk.FLAT, highlightthickness = 0 )
        ttk.Style().configure( 'Treeview', **o )
        # ttk.Style().configure( 'Treeview' )
        ttk.Style().configure( 'TText', **o )
        ttk.Style().configure( 'TButton', **o )
        ttk.Style().configure( 'TButton', relief = tk.RAISED, width = 10 )
        self.menuframe = ttk.Frame( self.master )
        self.menuframe.grid( row = 0 )

        self.buttonframe = ttk.Frame( self.menuframe )
        self.buttonframe.grid( row = 0 )

        self.process = ttk.Button( self.buttonframe, text = 'Process', command = self.process_canvas )
        self.process.grid( column = 1, row = 0, padx = 5 )

        self.reset = ttk.Button( self.buttonframe, text = 'reset', command = self.reset_canvas )
        self.reset.grid( column = 2, row = 0, padx = 5 )

        self.undo = ttk.Button( self.buttonframe, text = 'undo', command = self.undo )
        self.undo.grid( column = 3, row = 0, padx = 5 )

        self.quit = ttk.Button( self.buttonframe, text='QUIT', command = self.master.destroy )
        self.quit.grid( column = 4, row = 0, padx = 5 )

        self.reload = ttk.Button( self.buttonframe, text='RELOAD', command = self.master.reloadit )
        self.reload.grid( column = 5, row = 0, padx = 5 )


        self.contentframe = ttk.Frame( self.master )
        self.contentframe.grid( column = 0, row = 1 )

        self.treeframe = ttk.Frame( self.contentframe )
        self.treeframe.grid( column = 0, row = 0, rowspan = 2, padx = 5 )


        self.tree = ttk.Treeview( self.treeframe, height = 47 )

        self.tree['columns'] = ('one')#, 'two')
        self.tree.column( '#0', width = 270, minwidth = 270, stretch = tk.NO )
        # self.tree.column( 'one', width = 150, minwidth = 150, stretch = tk.NO )

        self.tree.heading( '#0',text = 'Name',anchor = tk.W )
        # self.tree.heading( 'one', text='Description', anchor = tk.W )

        self.build_folders()

        self.tree.bind( '<<TreeviewSelect>>', self.get_object_description )

        self.create_canvas()



        o = {
            'background': '#333333',
            'foreground': '#c78626',
            'relief': tk.FLAT,
            'width': 30,
            'borderwidth': 0,
            'highlightthickness': 0
        }


        self.infoframe = ttk.Frame( self.contentframe )
        self.infoframe.grid( column = 1, row = 0, 
            sticky = tk.N + tk.S + tk.W + tk.E, pady = 5 )

        self.infotext = tk.Text( self.infoframe, **o, wrap = tk.WORD, 
            font = ('Consolas', 13), state = tk.DISABLED, height = 10 )
        self.infotext.grid( column = 0, row = 0, sticky = tk.W )

        self.infobox = tk.Listbox( self.infoframe, **o, height = 13 )
        self.infobox.grid( column = 1, row = 0, sticky = tk.W, padx = 5 )

        self.sacred = ttk.Button( self.infoframe, text = 'sacred thing', 
            command = self.print_sacred  )
        self.sacred.grid( column = 2, row = 0 )

    def print_sacred( self ):
        o = {
            'background': self.framebgcolor,
            'relief': tk.FLAT,
            'borderwidth': 0,
            'height': 5 * self.oom,
            'width': 100,
            'highlightthickness': 0
        }
        self.canvas2 = tk.Canvas( self.infoframe, **o )
        self.canvas2.grid( column = 3, row = 0 )

        image = self.blueprints[self.currentitem].tile
        if image is not None:
            image = image.image
            image = image.resize( (image.size[0] * self.oom//3, image.size[1] * self.oom//3))
            self.image = image = ImageTk.PhotoImage( image )
            self.canvas2.create_image( 0,0, image = image )
        o = {
            'background': '#333333',
            'foreground': '#c78626',
            'relief': tk.FLAT,
            'width': 30,
            'borderwidth': 0,
            'highlightthickness': 0
        }

        self.infotext1 = tk.Text( self.infoframe, **o, wrap = tk.WORD, 
            font = ('Consolas', 13), state = tk.NORMAL, height = 10 )
        self.infotext1.grid( column = 4, row = 0, sticky = tk.W )

        xtag = self.blueprints[self.currentitem].attributes.get( 'xtag' )
        text = 'NONE'
        if xtag is not None:
            text = xtag['TextFragments']['SacredThing']
        self.infotext1.insert( '1.0', text )


    def create_canvas( self ):


        width = 80 * self.oom
        height = 25 * self.oom

        self.canvas = zooming.Zoom_Canvas( master = self.contentframe, 
            oom = self.oom, width = width, height = height, 
            background = self.canvasbackground, highlightthickness = 0 )

        self.canvas.grid( column = 1, row = 1, sticky = tk.N )


        self.canvas.bind( '<ButtonRelease-1>', self.stopdrawing )
        self.canvas.bind( '<Button-1>', self.callback )
        self.canvas.bind( '<B1-Motion>', self.callback )

        for w in range( 0, width, self.oom ):
            for h in range( 0, height, self.oom ):
                bbox = (w + self.oom/3, h + self.oom/3, w + 2*self.oom/3, h + 2*self.oom/3)
                self.canvas.create( shape = 'oval', bbox = bbox, 
                fill = '#614112', tags = 'dot', outline = self.canvasbackground)


        self.canvas.bind( '<Button-3>', self.getinfo )



    def build_folders( self, level = None ):
        folders = {'': ''}


        for name, info in self.blueprints.items():
            ancestors = info.ancestors
            descendants = info.descendants

            for ancestor in ancestors:
                ancestorname = ancestor.name

                if ancestorname == 'Object':
                    continue
                
                parent = ancestors[ancestors.index( ancestor ) - 1].name

                if parent == 'Object':
                    parent = ''

                if folders.get( ancestorname ) is None:
                    folders[ancestorname] = self.tree.insert( folders[parent], 1, text = ancestorname )


        self.tree.grid()



    def getinfo( self, event ):
        self.infobox.delete( 0, tk.END )
        d = .1
        x = event.x
        y = event.y
        o = {'x1': x - d, 'y1': y - d, 'x2': x + d, 'y2': y + d }
        items = self.canvas.find_overlapping( **o )


        regex = re.compile( r'object=(.*)' )

        for item in items[::-1]:
            tags = self.canvas.gettags( item )
            tags = list( filter( regex.match, tags ))

            if tags == []:
                return

            else:
                tag = tags[0].split( '=' )[1]
                self.infobox.insert( items.index( item ) + len( items ), tag )





