"""
A collection of methods to provide functionality for reading and writing
NetPBM images.

Functions:

get_info() -- get header details from a NetPBM file.
parse_image() -- read in data from any NetPBM file.
"""
import os.path
import string
import sys
from PIL import Image
import array


def get_info(path_or_file):

    # if path_or_file is file, assign to image_file and seek to start of file
    if isinstance(path_or_file, file):
        image_file = path_or_file
        image_file.seek(0, 0)

    # otherwise open the file
    else:
        # Check that file path points to a path
        if os.path.isfile(path_or_file):
            image_file = open(path_or_file, 'rb')
        else:
            sys.stderr.write("Invalid file path.\n")
            return

    # Read in the file type, if it is not valid then return
    file_type = image_file.read(2)
    if file_type not in ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']:
        sys.stderr.write("Invalid file type.\n")
        return

    # Discard comments
    byte = image_file.read(1)
    while byte is '#':
        image_file.readline()
        byte = image_file.read(1)

    # Return if there is no whitespace separating the dimensions from the type
    if byte not in string.whitespace:
        sys.stderr.write("Whitespace missing between type and dimensions.\n")
        return

    width, height, max_val = "", "", ""
    finished = 0

    # Read in dimensions and max value, discarding comments
    while not finished:
        byte = image_file.read(1)

        if byte == '#':
            image_file.readline()
            continue

        if byte in string.whitespace:
            continue

        if byte in string.digits:
            if width is "":
                width = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    width += byte
                    byte = image_file.read(1)
            elif height is "":
                height = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    height += byte
                    byte = image_file.read(1)
                if file_type in ['P1', 'P4']:
                    max_val = "255"
                    finished = 1
            elif max_val is "":
                max_val = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    max_val += byte
                    byte = image_file.read(1)
                finished = 1

        else:
            sys.stderr.write("Invalid char found: " + byte + "\n")
            return

    # If width or height read in are not valid then return None
    if not width.isdigit() or not height.isdigit() or not max_val.isdigit():
        sys.stderr.write("Invalid width, height or max_val.\n")
        return

    # Discard any comments remaining before the image data
    while byte is '#':
        image_file.readline()
        byte = image_file.read(1)

    # Check the last byte before the image data is whitespace
    if byte not in string.whitespace:
        sys.stderr.write("Invalid whitespace in file.\n")
        return

    return file_type, (int(width), int(height)), int(max_val)


def _P1_parser(image_file):

    # Read in image dimensions
    (width, height) = get_info(image_file)[1]
    dimensions = (width, height)

    # Create an image
    image = Image.new("RGB", dimensions, "white")

    # Read in image data
    image_str = []
    for line in image_file.readlines():
        line = line.strip()
        image_str.append(line)

    # Convert image_str into a string rather than a list of strings.
    image_str = ''.join(image_str)

    # Set black pixels
    for x in range(width):
        for y in range(height):
            if image_str[y * width + x] is '1':
                image.putpixel((x, y), 0)

    return image


def _P2_parser(image_file):

    t, (width, height), max_val = get_info(image_file)
    dimensions = (width, height)

    image1 = Image.new("L", dimensions, "white")

    image = []
    imagestr = []

    for line in image_file.readlines():
        line = line.replace('\n', ' ')
        imagestr.append(line)
    imagestr = ''.join(imagestr)
    imagestr = imagestr.split()

    #create matrix as list of lists
    i = 0
    while i < height:
        b = imagestr[(width*i):((width*i)+width)]
        image.append(b)
        i += 1

    print image

    for y in range(height):
        for x in range(width):
            a = image[y][x]
            colour = ((255/max_val)+((255/max_val)*int(a)))
            image1.putpixel((x, y), colour)

    return image1


#def P3_parser(image_file):


def _P4_parser(image_file):

    # Get the image dimensions
    (width, height) = get_info(image_file)[1]
    dimensions = (width, height)

    # Create an image to hold the image data
    image = Image.new('L', dimensions, 0)

    # Need to pad width out to 8 bits (rows are stored in full bytes).
    row_length = width/8
    if width % 8 is not 0:
        row_length = (width + 8 - width % 8)/8

    # Read in all the image data.
    contents = image_file.read(row_length*height)

    # Loop through each bit read in and convert it to a byte.
    data = ""
    for i in range(height):
        for j in range(width):
            position = i * row_length + j/8
            if ord(contents[position]) & (1 << 7 - j % 8):
                data += chr(0)
                #sys.stdout.write('X')
            else:
                data += chr(255)
                #sys.stdout.write('.')
        #sys.stdout.write('\n')

    # Populate the image with the data
    image.putdata(data)

    return image


def _P5_parser(image_file):

    # Get the image dimensions
    t, (width, height), max_val = get_info(image_file)
    dimensions = (width, height)

    # Create an image to hold the image data
    image = Image.new('L', dimensions, 0)

    # Loop through the pixel data and set the pixels in the image
    for y in range(height):
        for x in range(width):

            pixel = ord(image_file.read(1))
            if max_val > 255:
                pixel += 256 * ord(image_file.read(1))

            if pixel > max_val:
                pixel = max_val
            pixel = (pixel * 255)/max_val

            image.putpixel((x, y), pixel)

    return image


#def P6_parser(image_file):


def parse_image(image_file):

    # Read in the file info
    image_info = get_info(image_file)

    # If there was an error retrieving the image info then return
    if image_info is None:
        sys.stderr.write("Image header info not retrieved.\n")
        return

    # Set file type and then selected parser based on file type
    file_type = image_info[0]
    parser = globals().get("_" + file_type + "_parser")

    # If parser not available the return
    if not parser:
        sys.stderr.write("Parser for " + file_type + " not found.\n")
        return

    #return resize_image(parser(image_file))
    return parser(image_file)


# Move to an image processing module
def resize_image(image):

    (width, height) = image.size
    if (width, height) is (360, 32):
        return

    im = Image.new("L", (360, 32), "black")

    #TODO Compress this function (it's kind of messy)

    if width >= 360 and height >= 32:
        x = (width - 360) / 2
        y = (height - 32) / 2
        image = image.crop((x, y, x+360, y+32))
        im.paste(image)

    if width < 360 and height < 32:
        im.paste(image, (180 - width/2, 16 - height/2))

    elif width < 360:
        y = (height - 32) / 2
        image = image.crop((0, y, width, y+32))
        im.paste(image, (180 - width/2, 0))

    elif height < 32:
        x = (width - 360) / 2
        image = image.crop((x, 0, x+360, height))
        im.paste(image, (0, 16 - height/2))

    return im


# Move to an image processing module
def image_to_data(image):

    image = resize_image(image)
    data = [array.array('B', [0]*128) for i in range(90)]
    image_data = list(image.getdata())

    width = 360

    # loop through each column of pixels
    for i in range(width):
        col = image_data[i::width]
        sub_col = [col[x % 2 * 16 + x / 2:(x % 2 + 1) * 16:2] for x in range(4)]

        #loop through each bit of the col
        for j in range(8):
            #break col into 4 lots of 8 pixels
            for k in range(4):
                byte = 0
                for l in range(8):
                    if sub_col[k][l] & (1 << j):
                        #TODO SHOULD THIS BE (1 << 7-l)??
                        byte |= (1 << l)
                data[i/4][i%4*32+j*4+k] = byte

    return data







