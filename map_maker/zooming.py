# -*- coding: utf-8 -*-
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.
# pulled from https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan
# https://github.com/foobar167/junkyard/tree/master/manual_image_annotation1
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class AutoScrollbar( ttk.Scrollbar ):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set( self, lo, hi ):
        if float( lo ) <= 0.0 and float( hi ) >= 1.0:
            self.grid_remove( )
        else:
            self.grid( )
            ttk.Scrollbar.set( self, lo, hi )

    def pack( self, **kw ):
        raise tk.TclError( 'Cannot use pack with this widget' )

    def place( self, **kw ):
        raise tk.TclError( 'Cannot use place with this widget' )

class Zoom_Canvas( tk.Canvas ):
    ''' Advanced zoom of the image '''
    def __init__( self, master, oom, **kwargs ):
        ''' Initialize the main Frame '''
        self.master = master
        self.images = {}
        self.images_raw = []
        self.oom = oom
        # Vertical and horizontal scrollbars for canvas
        # vbar = AutoScrollbar( self.master, orient = 'vertical' )
        # hbar = AutoScrollbar( self.master, orient = 'horizontal' )
        # vbar.grid( row = 0, column = 1, sticky = 'ns' )
        # hbar.grid( row = 1, column = 0, sticky = 'we' )

        # Create canvas and put image on it
        # tk.Canvas.__init__( self.master, xscrollcommand = hbar.set, 
        #     yscrollcommand = vbar.set, **kwargs )
        tk.Canvas.__init__( self, self.master, **kwargs )

        self.grid( row = 0, column = 0, sticky = 'nswe' )
        self.update()  # wait till canvas is created

        # vbar.configure( command = self.scroll_y )  # bind scrollbars to the canvas
        # hbar.configure( command = self.scroll_x )

        # Make the canvas expandable
        self.master.rowconfigure( 0, weight = 1 )
        self.master.columnconfigure( 0, weight = 1 )

        # Bind events to the Canvas
        # self.bind( '<Configure>', self.show_image )  # canvas is resized
        # self.bind( '<ButtonPress-3>', self.move_from )
        # self.bind( '<B3-Motion>', self.move_to )
        # self.bind( '<MouseWheel>', self.wheel )  # with Windows and MacOS, but not Linux
        # self.bind( '<Button-5>', self.wheel )  # only with Linux, wheel scroll down
        # self.bind( '<Button-4>', self.wheel )  # only with Linux, wheel scroll up

        # self.image = Image.open( path )  # open image
        self.width, self.height = (100,100)
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        # self.container = self.create_rectangle( 0, 0, 240, 750, width = 0 )
        # Plot some optional random rectangles for the test purposes
        # minsize, maxsize, number = 5, 20, 10
        # for n in range( number ):
        #     x0 = random.randint( 0, self.width - maxsize )
        #     y0 = random.randint( 0, self.height - maxsize )
        #     x1 = x0 + random.randint( minsize, maxsize )
        #     y1 = y0 + random.randint( minsize, maxsize )
        #     color = ( 'red', 'orange', 'yellow', 'green', 'blue' )[random.randint( 0, 4 )]
        #     self.create_rectangle( x0, y0, x1, y1, fill = color, activefill = 'black' )
        # self.show_image( )

    def scroll_y( self, *args, **kwargs ):
        ''' Scroll canvas vertically and redraw the image '''
        self.yview( *args, **kwargs )  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x( self, *args, **kwargs ):
        ''' Scroll canvas horizontally and redraw the image '''
        self.xview( *args, **kwargs )  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from( self, event ):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.scan_mark( event.x, event.y )

    def move_to( self, event ):
        ''' Drag ( move ) canvas to the new position '''
        self.scan_dragto( event.x, event.y, gain = 1 )
        self.show_image()  # redraw the image

    def wheel( self, event ):
        ''' Zoom with mouse wheel '''
        x = self.canvasx( event.x )
        y = self.canvasy( event.y )
        bbox = self.bbox( self.container )  # get image area

        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            print( 'Ok! Inside the image' )
            pass
        else: 
            print( 'zoom only inside image area' )
            return

        scale = 1.0

        # Respond to Linux ( event.num ) or Windows ( event.delta ) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min( self.width, self.height )
            print( i )
            if int( i * self.imscale ) < 30:
                print( 'image is less than 30 pixels' ) 
                return

            self.imscale /= self.delta
            scale        /= self.delta

        if event.num == 4 or event.delta == 120:  # scroll up
            i = min( self.winfo_width(), self.winfo_height())
            if i < self.imscale:
                print( '1 pixel is bigger than the visible area' )
                return  

            self.imscale *= self.delta
            scale        *= self.delta

        self.scale( 'all', x, y, scale, scale )  # rescale all canvas objects
        self.show_image( )

    def create( self, **kwargs ):
        shape = kwargs['shape']
        del kwargs['shape']

        bbox = kwargs.get( 'bbox' )
        position = kwargs.get( 'position' )

        if bbox is not None:
            del kwargs['bbox']
            x0, y0, x1, y1 = bbox
            getattr( self, 'create_' + shape )( x0, y0, x1, y1, **kwargs )

        elif position is not None:
            del kwargs['position']
            x0, y0 = position

            image_raw = kwargs['image']
            width, height = image_raw.size
            ratio = self.oom / height
            image = image_raw.resize( (int( width * ratio ), self.oom ) )
            self.image = image = ImageTk.PhotoImage( image_raw )
            kwargs['image'] = image

            newid = getattr( self, 'create_' + shape )( x0, y0, **kwargs )
            self.images[newid] = {
                'image': self.image,
                'raw': image_raw
            }

        else:
            return

        if shape == 'image':
            self.images[newid]

        x0, y0, x1, y1 = self.bbox( tk.ALL )
        self.container = self.create_rectangle( x0, y0, x1, y1, width = 0 )


    def show_image( self, event = None ):
        print( 'Show image on the Canvas' )
        bbox1 = self.bbox( self.container )  # get image area

        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = ( bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1 )
        bbox2 = ( self.canvasx( 0 ),  # get visible area of the canvas
                 self.canvasy( 0 ),
                 self.canvasx( self.winfo_width( ) ),
                 self.canvasy( self.winfo_height( ) ) )

        bbox = [min( bbox1[0], bbox2[0] ), min( bbox1[1], bbox2[1] ),  # get scroll region box
                max( bbox1[2], bbox2[2] ), max( bbox1[3], bbox2[3] )]
        print( bbox1, bbox2, bbox, sep = '\n')
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]

        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]

        self.configure( scrollregion = bbox )  # set scroll region

        x1 = max( bbox2[0] - bbox1[0], 0 )  # get coordinates ( x1,y1,x2,y2 ) of the image tile
        y1 = max( bbox2[1] - bbox1[1], 0 )
        x2 = min( bbox2[2], bbox1[2] ) - bbox1[0]
        y2 = min( bbox2[3], bbox1[3] ) - bbox1[1]

        if int( x2 - x1 ) > 0 and int( y2 - y1 ) > 0:  # show image if it in the visible area
            print('sdfsdfsdf')
            x = min( int( x2 / self.imscale ), self.width )   # sometimes it is larger on 1 pixel...
            y = min( int( y2 / self.imscale ), self.height )  # ...and sometimes not

            temp = {}
            for imageid in self.images:
                bbox = self.bbox( imageid )
                image_raw = self.images[imageid]['raw']

                new_image = image_raw.crop(( int( x1 / self.imscale ), 
                    int( y1 / self.imscale ), x, y ))
                imagetk = ImageTk.PhotoImage( new_image.resize(( int( x2 - x1 ), int( y2 - y1 ))))
                # imageid = self.create_image( max( bbox2[0], bbox1[0] ), max( bbox2[1], bbox1[1] ),
                #                                 anchor = 'nw', image = imagetk )
                imageid = self.create_image( bbox[0], bbox[1],
                                                anchor = 'nw', image = imagetk )

                self.lower( imageid )  # set image into background
                self.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
                temp[imageid] = {'raw': image_raw, 'image': self.imagetk}

            self.images = {**self.images, **temp}
