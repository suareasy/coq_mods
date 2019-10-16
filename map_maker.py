import tkinter as tk
from tkinter import ttk
from lxml.etree import *
from PIL import Image, ImageTk
import time, importlib, re
import functools, operator, sys
import parse_blueprint


class Application( tk.Frame ):
    def __init__( self, master = None, oom = 10 ):
        super().__init__( master )
        self.master = master
        self.draw = False
        self.oom = oom
        self.recentchanges = []
        self.currenttime = 0
        self.currenttimetag = None
        self.drawing = False
        self.color = None
        self.image = None
        self.blueprints = parse_blueprint.main()
        self.folders = None
        self.images = {}
        self.currentlocation = None

    def setimage( self, res ):

        name = self.get_tree_selection()

        if name is None:
            return

        object = self.blueprints.find( './/object[@name="{}"]'.format( name ))

        if object is not None:
            imagepath = object.attrib['image']

        tags = ('object=' + name, 'item', self.currenttimetag)

        if imagepath != 'None':
           

            image = Image.open( '/home/dsuarez/Downloads/textures/' + imagepath.lower() )
            width, height = image.size
            ratio = self.oom / height
            image = image.resize( (int( width * ratio ), self.oom ) )
            self.image = image = ImageTk.PhotoImage( image )
            newid = self.canvas.create_image( (res['x'][0],res['y'][0]), 
                image = image, anchor = tk.NW, tags = tags )

            self.images[newid] = self.image
        else:

            color = 'yellow'

            newid = self.canvas.create_rectangle( res['x'][0], res['y'][0], 
                res['x'][1], res['y'][1], fill = color, tags = tags )


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
            
            coords = self.canvas.coords( item )

            if coords[0] != 0:
                res['x'].append( coords[0] )

            else:
                res['y'].append( coords[-1] )

        cellboundaries.sort()
        res['x'].sort()
        res['y'].sort()

        if event.type == '6':
            if self.currentlocation == res:
                    return

            else:
                self.currentlocation = res

        if len( res['x'] ) == 1:
            res['x'] = [0] + res['x']

        cx = cellboundaries[2]
        cy = cellboundaries[0]

        cell = self.canvas.find_closest( x, y )

        self.setimage( res )




        
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
            return self.tree.item( selection[0] )['text']


    def get_object_description( self, event ):
        name = self.get_tree_selection()

        if name is None:
            return


        object = self.blueprints.find( './/object[@name="{}"]'.format( name ))
        text = object.attrib['description']

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

        ttk.Style().configure( 'TFrame', background = '#525252', 
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

        self.contentframe = ttk.Frame( self.master )
        self.contentframe.grid( column = 0, row = 1 )

        self.treeframe = ttk.Frame( self.contentframe )
        self.treeframe.grid( column = 0, row = 0, rowspan = 2, padx = 5 )


        self.tree = ttk.Treeview( self.treeframe, height = 52 )

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
            font = ('Consolas', 13), state = tk.DISABLED, height = 8 )
        self.infotext.grid( column = 0, row = 0, sticky = tk.W, pady = 10 )

        self.infobox = tk.Listbox( self.infoframe, **o, height = 10 )
        self.infobox.grid( column = 0, row = 1, sticky = tk.W )


    def create_canvas( self ):


        canvaswidth = 80 * self.oom
        canvasheight = 25 * self.oom

        self.canvas = tk.Canvas( self.contentframe, width = canvaswidth, 
            height = canvasheight, borderwidth = 0, relief = tk.FLAT, 
            background = '#7d7d7a', highlightthickness = 0 )

        self.canvas.bind( '<ButtonRelease-1>', self.stopdrawing )
        self.canvas.bind( '<Button-1>', self.callback )
        self.canvas.bind( '<B1-Motion>', self.callback )

        self.canvas.grid( column = 1, row = 1, sticky = tk.N )

        for w in range( 0, canvaswidth, self.oom ):
            for h in range( 0, canvasheight, self.oom ):
                self.canvas.create_rectangle( w, h, w + self.oom, h + self.oom, 
                    fill = '#c7c7c7', tags = 'base' )

        for w in range( 0, canvaswidth + self.oom, self.oom ):
            self.canvas.create_line( w, 0, w, canvasheight, 
                fill = '#7d7d7a', tags = ('coordinates',w / self.oom ))
        
        for h in range( 0, canvasheight + self.oom, self.oom ):
            self.canvas.create_line( 0, h, canvaswidth, h, 
                fill = '#7d7d7a', tags = ('coordinates', h / self.oom ))



        self.canvas.bind( '<Button-3>', self.getinfo )



    def build_folders( self, level = None ):
        if self.folders is None:
            self.folders = {}


        if level is None:
            blueprints = self.blueprints.getchildren()[0]
            parent = ''
            self.folders[parent] = ''

        else:
            blueprints = self.blueprints.find( './/object[@name="{}"]'.format( level ))
            parent = blueprints.getparent().attrib['name']
            if parent == 'Object':
                parent = ''

        for blueprint in blueprints:
            name = blueprint.attrib['name']
            if len( blueprint ) > 0:
                self.folders[name] = self.tree.insert( self.folders[parent], 1, '', text = name )
                self.build_folders( name )
            else:
                self.tree.insert( self.folders[parent], tk.END, text = name )


    
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



orderofmagnitude = 30

width = 100 * orderofmagnitude
height = 30 * orderofmagnitude 

colors = ['red', 'green', 'blue', 'yellow']
mapping = {'WoodWall' + str(i): colors[i] for i in range( len( colors ))}

root = tk.Tk()
root.geometry( str( width ) + 'x' + str( height ))
root.configure( background = '#525252' )
app = Application( master = root, oom = orderofmagnitude )
app.create_menu_widgets()
app.mainloop()

