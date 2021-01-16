import tkinter as tk
from tkinter import ttk

class Tree( ttk.Frame ):
    def __init__( self, master, blueprints ):
        self.tree = ttk.Treeview( master, height = 47 )

        self.tree['columns'] = ('one')#, 'two')
        self.tree.column( '#0', width = 270, minwidth = 270, stretch = tk.NO )
        # self.tree.column( 'one', width = 150, minwidth = 150, stretch = tk.NO )

        self.tree.heading( '#0',text = 'Name',anchor = tk.W )
        # self.tree.heading( 'one', text='Description', anchor = tk.W )

        self.build_folders( blueprints )

    def build_folders( self, blueprints, level = None ):
        folders = {'': ''}


        for name, info in blueprints.items():
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
                    if folders.get( parent ) is None:
                        folders[parent] = self.tree.insert( folders[''], 1, text = parent )
                    folders[ancestorname] = self.tree.insert( folders[parent], 1, text = ancestorname )


        self.tree.grid()
