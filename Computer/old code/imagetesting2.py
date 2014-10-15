from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#this image works
#fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p1-pbm-ascii\\TestPattern 32x32 p1.pbm", "rU")

#this does not
fp = open("C:\\Users\\Megan\\Documents\\ENGG2800\\engg2800-team33\\Computer\\p1-pbm-ascii\\It works 145x32 p1.pbm", "rU")
image = []
imagestr = []
#im = Image.open(fp)

#read in first two lines of image(type and size)
print fp
img_type = fp.readline()
img_size = fp.readline()

#get image size
print img_type
image_size=[]
for s in img_size.split():
    image_size.append(int(s))
size=(image_size[0], image_size[1])

#print fp.readlines()

#append matrix with image data
for line in fp.readlines():
    line=line.strip()
    imagestr.append(line)
imagestr=''.join((imagestr))

#print imagestr[:(size[0]):]
#image.append(imagestr[:size[0]])

print imagestr


#append matrix with image data
#for line in fp.readlines():
#    image.append(line)
    #sys.stdout.write(line)


    
fp.close()
im = Image.new("RGB", size, "white")
draw = ImageDraw.Draw(im)
#print image

y=0

for row in image:
    x=0
    for col in row:
        a=image[y][x]
        if a == '0':
            draw.point((x,y), fill="black")
        x+=1
    y+=1
#im.show()
#fp.readlines()
