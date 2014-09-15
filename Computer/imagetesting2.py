from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p1-pbm-ascii\\TestPattern 32x32 p1.pbm", "rb")
image = []
#im = Image.open(fp)
print fp
#im.show()
img_type = fp.readline()
img_size = fp.readline()
for line in fp:
    line = line.strip()
    image.append(list(line))

#Matrix Size
i=0
j=0
for row in image:
    i=i+1
for col in image[1]:
    j=j+1

fp.close()
im = Image.new("RGB", (j, i), "white")
draw = ImageDraw.Draw(im)
#print image

x=0
y=0

for row in image:
    x=0
    for col in row:
        a = image[x][y]
        if a == '1':
            draw.point((x,y), fill="black")
        x=x+1
    y=y+1
im.show()
#fp.readlines()
