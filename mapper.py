import csv
from lxml.etree import *

def tonone( s ):
    
    if s.lower() == 'none':
        return None

    return s

def getmappings( mappingfile ):
    with open( mappingfile, newline = '' ) as f:
        
        next( f )
        rawmappings = list( csv.reader( f, delimiter = ',' ))
        
    mappings = {x[0]:tonone( x[1] ) for x in rawmappings}
    
    return mappings


def main( imagefile, mappingfile ):

    mappings = getmappings( mappingfile )

    parser = HTMLParser()
    tree = parse( imagefile, parser )
    data = tree.getroot().find( './/table' )

    w = len( data )
    l = len( data[0] )

    root = Element( 'Map', {
        'Width': str( w ),
        'Length': str( l )
    })

    root.text = '\n\t'

    for y in range( w ):

        for x in range( l ):
            
            celldata = data[y][x].attrib['bgcolor']

            cellement = SubElement( root, 'cell', {
                'X': str( x ),
                'Y': str( y )
            })

            cellement.tail = '\n\t'
            
            mapping = mappings.get( celldata )
            
            if mapping is not None:
                
                cellement.text = '\n\t\t'
                
                obj = SubElement( cellement, 'object', {'name': mapping} )
                obj.tail = '\n\t'

    root[-1].tail = '\n'

#    print( tostring( root ).decode( 'utf-8' ))
    with open( output, 'w' ) as f:
        f.write( tostring( root ).decode( 'utf-8' ))

main( 'test.html', 'mappings.csv', 'test.rpm' )
