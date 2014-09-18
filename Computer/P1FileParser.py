from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#this image works
#fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p1-pbm-ascii\\TestPattern 32x32 p1.pbm", "rU")

#this image also works
fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p4-pbm-binary\\TestPattern 32x32 p4.pbm", "rU")
print fp.readlines()
#check file opened
print fp

#initialise lists
image = []
imagestr = []

#read in first two lines of image(type and size)
img_type = fp.readline()
img_size = fp.readline()

#get image size
print img_type
image_size=[]
for s in img_size.split():
    image_size.append(int(s))
size=(image_size[0], image_size[1])
(w,h)=size
print size

#append imagestring with image data
for line in fp.readlines():
    line=line.strip()
    imagestr.append(line)
imagestr=''.join((imagestr))

#create matrix as list of lists (create image from imagestring)
i=0
while i<h:
    b = imagestr[(w*i):((w*i)+w)]
    image.append(b)
    i+=1
image=list(image)

#close file   
fp.close()

#draw new image
im = Image.new("RGB", size, "white")
draw = ImageDraw.Draw(im)

#draw image
y=0
for row in image:
    x=0
    for col in row:
        a=image[y][x]
        if a == '0':
            draw.point((x,y), fill="black")
        x+=1
    y+=1
im.show()
