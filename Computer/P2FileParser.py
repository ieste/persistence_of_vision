from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#Greyscale
#c = (max_val/255)

#this image works
#fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p2-pgm-ascii\\It works 145x32 p2.pgm", "rU")

#this image also works
#fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p2-pgm-ascii\\TestPattern 32x32 p2.pgm", "rU")

fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p2-pgm-ascii\\UQ logo-reverse-111x32 p2.pgm", "rU")
#check file opened
print fp

#initialise lists
image = []
imagestr = []

#read in first two lines of image(type and size)
img_type = fp.readline()
img_size = fp.readline()
max_val = int(fp.readline())

print img_type
print img_size
print max_val


#get image size
image_size=[]
for s in img_size.split():
    image_size.append(int(s))
size=(image_size[0], image_size[1])
(w,h)=size
print size

#append matrix with image data
for line in fp.readlines():
    line=line.replace('\n', ' ')
    imagestr.append(line)
imagestr=''.join((imagestr))
imagestr=imagestr.split()

#create matrix as list of lists
i=0
while i<h:
    b = imagestr[(w*i):((w*i)+w)]
    image.append(b)
    i+=1

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
        colour = ((255/max_val)+((255/max_val)*int(a)))
        draw.point((x,y), fill=(colour, colour, colour))
        x+=1
    y+=1
im.show()
