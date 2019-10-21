import hagadias.gameroot as hagadias
from map_maker import *
import sys
args = sys.argv

if len( args ) != 2:
    print( ' I need a game path. One for blue prints and one for the tool kit.' )
    quit()

else:
    
    gamepath = args[1]

root = hagadias.GameRoot( gamepath )

qoroot, qindex = root.get_object_tree()


orderofmagnitude = 30

width = 100 * orderofmagnitude
height = 30 * orderofmagnitude 

colors = ['red', 'green', 'blue', 'yellow']
mapping = {'WoodWall' + str(i): colors[i] for i in range( len( colors ))}

root = tk.Tk()
root.geometry( str( width ) + 'x' + str( height ))
root.configure( background = '#525252' )
app = Application( master = root, oom = orderofmagnitude )
app.blueprints = qindex
app.create_menu_widgets()
app.mainloop()
