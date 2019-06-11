import csv
from lxml.etree import *

words = [
    'wall',
    'bridge',
    'river',
    'floor',
    'door'
]

mappings = {word[0]: word for word in words}


with open( 'Downloads/candy_kingdom.csv', newline='' ) as f:
    
    data = list( csv.reader( f ))


l = len( data[0] )
w = len( data )

root = Element( 'Map', {
    'Width': str( w - 2 ),
    'Length': str( l - 2 )
})

root.text = '\n\t'

for y in range( 1, w - 1 ):

    for x in range( 1, l - 1 ):
        
        celldata = data[y][x]

        cellement = SubElement( root, 'cell', {
            'X': str( x - 1 ),
            'Y': str( y - 1 )
        })

        cellement.tail = '\n\t'
        
        mapping = mappings.get( celldata )
        
        if mapping is not None:
            
            cellement.text = '\n\t\t'
            
            obj = SubElement( cellement, 'object', {'name': mapping} )
            
            obj.tail = '\n\t'

root[-1].tail = '\n'

print( tostring( root ).decode( 'utf-8' ))
                

