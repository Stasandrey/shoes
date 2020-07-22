#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wand.drawing import Drawing, STYLE_TYPES
from wand.image import Image
import os
dm = "dmcode.png"

def generateSticker( model, size, gtin, serial, dmC ):
    lim = 1.7
    w = round( dmC.width * lim )
    h = round( dmC.height * lim )
    print( "%s %s %s %s"%( model, size, gtin, serial ) )
    dmCode = dmC.clone()
    dmCode.sample( w, h )
    img = Image( filename = "./maket.png" ).clone()
    draw = Drawing()
    draw.composite( operator = "over", left = 600, top = 70, width = dmCode.width,  height = dmCode.height, image = dmCode )
    draw.font_size = 110
    draw.text( 100, 240, model )
    draw.text( 240, 420, size )
    draw.font_size = 70
    draw.text( 50, 750, gtin[4 : 18] )
    draw.font_size = 50
    draw.text( 580, 630, gtin )
    draw.text( 680, 720, serial )
   
    draw( img )
    img.save( filename = "out.png" )
    dmCode.save( filename = "dout.png" )

# Reading text information
name = "./1.pdf"
os.system( 'pdf2txt %s > tmp_pdf.txt'%( name ) )
with open( "tmp_pdf.txt", "rt" ) as f:
    res = f.readlines()
data = []
for line in res:
    if line != "\n":
        if line != "0\n":
            if line != "\x0c":
                data.append( line.rstrip() )
print( data )
model = data[0][0 : data[0].find( '(' ) - 1]
size = data[0][data[0].find( '(' ) + 1 : data[0].find( ')' )]
gtin = data[1]
serial = data[2]

# Reading datamatrix code
tmp = Image( filename = "./1.pdf[0]", resolution = 300 )
tmp.convert( 'png' ) 
tmp.crop( 450, 150, 750, 450  )
generateSticker( model, size, gtin,  serial, tmp )

