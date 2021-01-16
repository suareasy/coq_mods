import tkinter as tk
from tkinter import ttk
import lxml.etree as etree
from PIL import Image, ImageTk
import time, importlib, re
import functools, operator, sys
import app.parts.zooming as zooming
import app.parts.themes as themes
from app.parts.infoframe import InfoFrame
from app.parts.map import Canvas
from app.parts.tiledirectory import Tree


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
        self.items = {}
        self.images = {}
        self.framebgcolor = '#525252'
        self.canvasbackground = '#141313'
        self.currentlocation = None
        self.wdiff = 16 * self.oom // 20
        self.hdiff = 24 * self.oom // 20

    def create_widgets( self ):


        ttk.Style().configure( 'TFrame', background = self.framebgcolor, 
            borderwidth = 0, relief = tk.FLAT, highlightthickness = 0 )
        ttk.Style().configure( 'Treeview', **themes.o )
        # ttk.Style().configure( 'Treeview' )
        ttk.Style().configure( 'TText', **themes.o )
        ttk.Style().configure( 'TButton', **themes.o )
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
        self.tree = Tree( self.treeframe, self.blueprints ).tree

        # self.tree = ttk.Treeview( self.treeframe, height = 47 )

        # self.tree['columns'] = ('one')#, 'two')
        # self.tree.column( '#0', width = 270, minwidth = 270, stretch = tk.NO )
        # # self.tree.column( 'one', width = 150, minwidth = 150, stretch = tk.NO )

        # self.tree.heading( '#0',text = 'Name',anchor = tk.W )
        # # self.tree.heading( 'one', text='Description', anchor = tk.W )

        # self.build_folders()

        self.tree.bind( '<<TreeviewSelect>>', self.get_object_description )

        self.create_canvas()

        self.infoframe = ttk.Frame( self.contentframe )
        self.infoframe.grid( column = 1, row = 0, 
            sticky = tk.N + tk.S + tk.W + tk.E, pady = 5 )

        self.infoframecontent = InfoFrame( self.infoframe )
        self.infobox = self.infoframecontent.infobox
        self.infobox.bind( '<<ListboxSelect>>', self.get_object_description )
        self.infobox.bind( '<Double-Button-1>', self.set_current_selection )


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
        items = self.canvas.find_overlapping( **self.currentlocation )
        item =  list( filter( lambda m: 'dot' in self.canvas.gettags( m ), items ))[0]

        self.canvas.itemconfig( item, fill = self.canvas['background'], 
        tags = ('dot', self.currenttimetag) )


        if image is not None:
            newid = self.canvas.create( shape = 'image', 
                position = (self.currentlocation['x1'], self.currentlocation['y1']), 
                image = image, anchor = tk.NW, tags = tags )

        else:

            color = 'yellow'

            coords = [y for x,y in self.currentlocation.items()]
            coords = [coords[0] + self.wdiff // 4, coords[1] + self.hdiff // 4, coords[2] - self.wdiff, coords[3] - self.hdiff]
            newid = self.canvas.create( shape = 'rectangle', bbox = coords, fill = color, tags = tags )

        


    def stopdrawing( self, event ):
        self.drawing = False

    def get_qud_cell( self, event ):
        x = event.x
        y = event.y
        wdiff = self.wdiff
        hdiff = self.hdiff
        xbar = ( x // wdiff ) * wdiff
        ybar = ( y // hdiff ) * hdiff
        o = {'x1': xbar, 'y1': ybar, 'x2': xbar + 2 * wdiff, 'y2': ybar + 2 * hdiff }
        return o

    def callback( self, event ):
        o = self.get_qud_cell( event )

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
        maproot = etree.Element( 'Map', {'Height': str( height ), 'Width': str( width )})
        maproot.text = '\n\t'
        for x in range( width ):
            for y in range( height ):
                
                e = etree.SubElement( maproot, 'cell', {'X': str( x ), 'Y': str( y )} )
                e.text = '\n\t\t'
                e.tail = '\n\t'
        with open( 'test.xml', 'w' ) as f:
            f.write( etree.tostring( maproot ).decode( 'utf-8' ))
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
            se = etree.SubElement( e, 'object', {'Name': name} )

            se.tail = '\n\t\t\t'
        #e[-1].tail = e.tail

        #maproot[-1].tail = '\n'

        # print( tostring( maproot ).decode( 'utf-8' ))
        with open( 'map1.rpm', 'w' ) as f:
            f.write( etree.tostring( maproot ).decode( 'utf-8' ))


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


    def set_current_selection( self, event ):
        selection = self.infobox.curselection()

        if selection == () or selection is None:
            return

        name = self.infobox.get(selection[0])

        objectid = self.items.get( name )

        self.currentitem = {
            'name': name,
            'id': objectid
        }
        
        self.tree.selection_set( objectid )


    def get_object_description( self, event ):

        name = None
        if event.widget.winfo_id() == self.infobox.winfo_id():
            selection = self.infobox.curselection()

            if selection == () or selection is None:
                return

            name = self.infobox.get(selection[0])


        else:
            name = self.get_tree_selection()
            if self.items.get( name ) is None:
                self.items[name] = self.tree.focus()


        if name is None:
            return

        local = {
            'name': name,
            'id': self.items[name]
        }

        self.canvas2 = self.infoframecontent.canvas2
        # if local != self.currentitem:
        #     self.currentitem = local

        # self.tree.selection_set( self.currentitem['id'] )

        object = self.blueprints.get( name )
        text = object.desc

        if text == 'None' or text is None:
            text = 'Sorry. There is no description for \'{}\''.format( name )

        self.infotext = self.infoframecontent.infotext
        self.infotext.config( state = tk.NORMAL )
        self.infotext.delete( '1.0', tk.END )
        self.infotext.insert( tk.END, text )

        self.infotext.config( state = tk.DISABLED )

        image = self.blueprints[name].tile

        if image is not None:
            image = image.image
            image = image.resize( (image.size[0] * self.oom//4, image.size[1] * self.oom//4))

            self.image = image = ImageTk.PhotoImage( image )

            self.canvas2.create_image( 100, 100, image = image, tags = 'image' )

        else:
            self.canvas2.delete( 'image' )

        # self.infotext1 = tk.Text( self.infoframe, **themes.o, wrap = tk.WORD, 
        #     font = ('Consolas', 13), state = tk.NORMAL, height = 10 )
        # self.infotext1.grid( column = 4, row = 0, sticky = tk.W )

        # xtag = self.blueprints[self.currentitem].attributes.get( 'xtag' )
        # text = 'NONE'
        # if xtag is not None:
        #     text = xtag['TextFragments']['SacredThing']
        # self.infotext1.insert( '1.0', text )
        





    def create_canvas( self ):
        self.canvas = Canvas( self.contentframe, self.wdiff, self.hdiff, self.oom ).canvas
        self.canvas.bind( '<ButtonRelease-1>', self.stopdrawing )
        self.canvas.bind( '<Button-1>', self.callback )
        self.canvas.bind( '<B1-Motion>', self.callback )
        self.canvas.bind( '<Button-3>', self.getinfo )
        # wdiff = self.wdiff
        # hdiff = self.hdiff
        # width = 80 * wdiff
        # height = 25 * hdiff

        # self.canvas = zooming.Zoom_Canvas( master = self.contentframe, 
        #     oom = self.oom, width = width, height = height, 
        #     background = self.canvasbackground, highlightthickness = 0 )

        # self.canvas.grid( column = 1, row = 1, sticky = tk.N )


        # self.canvas.bind( '<ButtonRelease-1>', self.stopdrawing )
        # self.canvas.bind( '<Button-1>', self.callback )
        # self.canvas.bind( '<B1-Motion>', self.callback )

        # r = 2
        # for w in range( wdiff//2, width, wdiff ):
        #     for h in range( hdiff//2, height, hdiff ):
        #         center = (w,h)
        #         # bbox = (w + wdiff/3, h + hdiff/3, w + 2*wdiff/3, h + 2*hdiff/3)
        #         self.canvas.create( shape = 'circle', center = center, radius = 2, 
        #         fill = themes.canvas_fill, tags = 'dot', outline = self.canvasbackground)


        # self.canvas.bind( '<Button-3>', self.getinfo )






    def getinfo( self, event ):
        self.infobox.delete( 0, tk.END )

        o = self.get_qud_cell( event )
        items = self.canvas.find_enclosed( o )

        regex = re.compile( r'object=(.*)' )

        for item in items[::-1]:
            tags = self.canvas.gettags( item )
            tags = list( filter( regex.match, tags ))
            if tags == []:
                return

            else:
                tag = tags[0].split( '=' )[1]
                self.infobox.insert( items.index( item ) + len( items ), tag )





