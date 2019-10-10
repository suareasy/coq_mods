
from glob import glob
from lxml.etree import *
import re
from pprint import pprint

home = '/home/dsuarez/Downloads/'
CoQdir = home + '/Linux/CoQ_Data/StreamingAssets/Base/'


maps = glob( CoQdir + '*.rpm' )

if maps == []:
    print( 'Nothing found in {}'.format( CoQdir ))
    exit()

tilenames = {}
for map in maps: 

    tree = parse( map )
    root = tree.getroot()

    width = root.attrib['Width']
    height = root.attrib['Height']

    for x in range( int( width )):
        for y in range( int( height )):
            e = root.find( './/cell[@X="{0}"][@Y="{1}"]'.format( str( x ), str( y )))
            if e is not None:
                if len( e ) > 1:
                    print( tostring( e ).decode( 'utf-8' ))
                    # print( '-------------------\n')
                    # for child in e:
                    #     print( child.attrib['Name'] )
    continue

    src = map.split( '/' )[-1][:-4]
    print( src )
    with open( map, 'r' ) as f:
        data = f.read()

    matches = set( re.findall( r'<object\s*Name="(.*?)">', data ))

    for m in matches:
        if tilenames.get( m ) is None:
            tilenames[m] = 'COLOR'






