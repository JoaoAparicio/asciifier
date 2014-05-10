# interesting fonts
# http://www.lowing.org/fonts/

import StringIO
import sys
from PIL import Image, ImageFont, ImageDraw

from fontsizes import font2size, font2size2
import images2gif

scale = ["$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
         "@%#*+=-:. ",
         "@%#*+-:. ",
        ]

def rgb2scale(x, sc):
    return scale[sc][int(x/256.*len(scale[sc]))]

## this function has the following properties
## output size, in pixels, is the same as input
## allows for an input: number of horizontal chars. picks font size as a function of this
def asciify1pic(img, n_char_h=100):
    ## get pixel sizes of the input picture
    pic_h_pixels, pic_v_pixels = img.size
    ## compute the pixel width of the font
    char_h_pixels = int(1. * pic_h_pixels/n_char_h)
    ## given the font width, get the adecuate font size
    print 'char_h_pixels', char_h_pixels
    fontsize = font2size[char_h_pixels]
    font = ImageFont.truetype('monaco.ttf', fontsize)
    ## get pixel height of the font
    char_v_pixels = font.getsize('A')[1]
    ## comput how many characters there should be, vertically
    n_char_v = int(1. * pic_v_pixels/char_v_pixels)

#    print 'picture size: ', pic_h_pixels, pic_v_pixels
#    print 'char size: ', char_h_pixels, char_v_pixels
#    print 'number of chars: ', n_char_h, n_char_v
#    print 'fontsize: ', fontsize
#    print 'char size according to font.getsize: ', font.getsize('A')

    ## study if .thumbnail() should be used instead
    r = img.resize( (n_char_h,n_char_v) )
    r = r.convert(mode='L')

    #r = r.point(rgb2scale)
    result = []
    for i in range(0, n_char_v):
        result.append('')
        for j in range(0, n_char_h):
            result[i] = result[i] + rgb2scale(r.getpixel((j,i)),1)

    canvas = Image.new('RGB', (pic_h_pixels,pic_v_pixels), (255,255,255) )
    draw = ImageDraw.Draw(canvas)
    for n,line in enumerate(result):
        draw.text((0,0+n*char_v_pixels), line, (0,0,0), font=font)
    return canvas


## output size is always 400 pixels width
## height is picked to keep the input ratio
## output number of chars horitontally is always 100
def asciify1pic2(img):
    pic_h_pixels, pic_v_pixels = img.size

    ## size of output picture, in pixels
#    output_pixels_x = 400
#    output_pixels_x = 640
#    output_pixels_x = pic_h_pixels
    if pic_h_pixels > 640:
        output_pixels_x = 640
    else:
        output_pixels_x = pic_h_pixels
    output_pixels_y = int(1.* pic_v_pixels/pic_h_pixels * output_pixels_x)

    ## at fontsize 16 this font is 10x21
    ## at fontsize 10 this font is 6x13
    font = ImageFont.truetype('monaco.ttf', 6)
    font_x, font_y = font.getsize('A')

    ## size of output picture, in chars
    n_char_h= int(1. * output_pixels_x / font_x) ## = 40
    n_char_v = int(1. *  output_pixels_y / font_y)

#    r = img.resize( (n_char_h,n_char_v), Image.ANTIALIAS )
    r = img.resize( (n_char_h,n_char_v), Image.BILINEAR )
    r = r.convert(mode='L')

    result = []
    for i in range(0, n_char_v):
        result.append('')
        for j in range(0, n_char_h):
            result[i] = result[i] + rgb2scale(r.getpixel((j,i)),2)

    canvas = Image.new('RGB', (output_pixels_x,output_pixels_y), (255,255,255) )
    draw = ImageDraw.Draw(canvas)
    for n,line in enumerate(result):
        draw.text((0,0+n*font_y), line, (0,0,0), font=font)
    return canvas


def gif2ascii(img):
    duration = 1. * img.info['duration']/1000

    counter = 0
    collection = []
    current = img.convert('RGBA')
    while True:
        try:
#            current.save('original{:0>2}.png'.format(counter), 'PNG')
#            collection.append(current)
            asciified = asciify1pic2(current)
#            asciified.save('output%d.png' % counter, 'PNG')
            collection.append(asciified)
            img.seek(img.tell()+1)
            current = Image.alpha_composite(current, img.convert('RGBA'))
            counter += 1
        except EOFError:
            break

    buf = StringIO.StringIO()
    images2gif.writeGif(buf, collection, duration=duration)
    return buf

def gif2asciitest(img):
    duration = 1. * img.info['duration']/1000

    counter = 0
    collection = []
    current = img.convert('RGBA')
    while True:
        try:
#            current.save('original{:0>2}.png'.format(counter), 'PNG')
#            collection.append(current)
            asciified = asciify1pic2(current)
            asciified.save('output%d.png' % counter, 'PNG')
            collection.append(asciified)
            img.seek(img.tell()+1)
            current = Image.alpha_composite(current, img.convert('RGBA'))
            counter += 1
        except EOFError:
            break

#    images2gif.writeGif('test.gif', collection, duration=duration)
    buf = StringIO.StringIO()
    images2gif.writeGif(buf, collection, duration=duration)
    return buf



