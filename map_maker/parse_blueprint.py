from lxml import etree
from util import lxml_util
import re, functools, operator
import os, shutil


# had to convert &#(\d+) to \1 when parsing  xml
def main( blueprintpath, toolkitpath ):
    blueprints = 'ObjectBlueprints.xml'

    with open( blueprints, 'r' ) as f:
        data = f.read()

    data = re.sub( r'&#(\d+)', r'\g<1>', data )


    root = etree.fromstring( data )


    eve = root[0]


    res = etree.Element( 'blueprints' )

    for child in root[1:]:
        if type( child ) == etree._Comment:
            continue
        # print( etree.tostring( child ).decode( 'utf-8' ))
        name = child.attrib['Name']
        ancestorname = child.attrib['Inherits']

        part = {
            'render': child.find( './part[@Name="Render"]' ),
            'description': child.find( './part[@Name="Description"]' )
        }

        imagelocation = None
        if part['render'] is not None:
            imagelocation = part['render'].attrib.get( 'Tile' )

        if imagelocation is not None:
            if 'assets_content_textures_tiles_tile-9-4.png' in imagelocation:
                imagelocation = 'tiles/tile-9-4.png'

        description = None
        if part['description'] is not None:
            description = part['description'].attrib.get( 'Short' )
        
        ancestor = res.find( './/object[@name="{}"]'.format( ancestorname ))

        if ancestor is None:
            ancestor = etree.SubElement( res, 'object', {'name': ancestorname} )

        attributes = {
            'image': str( imagelocation ),
            'description': str( description ),
            'name': name
        }
        etree.SubElement( ancestor, 'object', attributes )

    lxml_util.indent( res, res )
    return( res )

def modify_texture_location( toolkitpath ):

    for thing in os.walk( toolkitpath + '/Textures' ):
        print( thing )

        cur, subdir, files = thing

        cur = cur + '/'

        moveto = toolkitpath + '/textures/' + cur[2:]


        for sd in subdir:
            os.makedirs( moveto + sd.lower())

        for f in files:
            curlocation = cur + f
            end = moveto + f
            end = end.lower()
            shutil.copy( curlocation, end )
            

#print( etree.tostring( res ).decode( 'utf-8' ))

# class BluePrints():
#     def __init__( self ):
#         self.blueprint = {}

#     def findkey( self, key, parentchain = None ):

#         self.getobject( parentchain )


#         if self.blueprints.get( key ) is not None:
#             return [key]

        
#         for pkey, content in self.blueprints:
#             if content.get( key ) is not None:
#                 parentchain += [pkey]

#     def getobject( self, mapping = None ):

#         if mapping.__hash__ is not None:
#             return self.blueprint.get( mapping, 'Nothing found for \'{}\''.format( mapping ))

#         elif type( mapping ) == list:
#             if mapping == []:
#                 return self.blueprint
#             try:
#                 res = functools.reduce( operator.getitem, mapping, self.blueprints )
#             except Exception as e:
#                 print( 'The mapping failed.' )
#                 print( e.args )

#         else:
#             print( 'Mapping should be hashable or a list of hashable keys' )
#             print( mapping )


#     def setobject( self, mapping, value ):

#         if mapping.__hash__ is not None:
#             return self.blueprints.get( mapping, 'Nothing found for \'{}\''.format( mapping ))

#         elif type( mapping ) == list:
#             self.getobject( mapping[:-1] )[mapping[-1]] = value
#             print( 'The value {} has been added.'.format( str( value )))

#         else:
#             print('meh')
