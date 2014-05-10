from PIL import Image
from asciify import asciify1pic
import images2gif
import sys


if len(sys.argv) != 3:
    print 'Usage: python', sys.argv[0], '<input.gif> <output.gif>'
    exit(1)

img = Image.open(sys.argv[1])
outputfile = sys.argv[2]

#asciify1pic(img, 100).save('asciified.png')
duration = 1. * img.info['duration']/1000

collection = []
while True:
    try:
        asciified = asciify1pic(img, 100)
        collection.append(asciified)
        img.seek(img.tell()+1)
    except EOFError:
        break

images2gif.writeGif(outputfile, collection, duration=duration)

