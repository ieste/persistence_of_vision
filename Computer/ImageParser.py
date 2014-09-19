import os.path
import string
import sys
from PIL import Image
import io


def get_info(path_or_file):

    #if path_or_file is
    if isinstance(path_or_file, file):
        image_file = path_or_file
        image_file.seek(0, 0)
    else:
        # Check that file path points to a path
        if os.path.isfile(path_or_file):
            image_file = open(path_or_file, 'rb')
        else:
            sys.stderr.write("Invalid file path.")
            return

    # Read in the file type, if it is not valid then return
    file_type = image_file.read(2)
    if file_type not in ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']:
        sys.stderr.write("Invalid file type.")
        return

    # Return if there is no whitespace separating the dimensions
    if image_file.read(1) not in string.whitespace:
        sys.stderr.write("Whitespace missing between type and dimensions.")
        return

    width = 0
    height = 0
    finished = 0

    while not finished:
        byte = image_file.read(1)

        if byte is '#':
            image_file.readline()
            continue

        if byte in string.whitespace:
            continue

        if byte in string.digits:
            if width is 0:
                width = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    width += byte
                    byte = image_file.read(1)
            elif height is 0:
                height = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    height += byte
                    byte = image_file.read(1)
                finished = 1

        else:
            sys.stderr.write("Invalid char found: " + byte)
            return

    # If width or height read in are not valid then return None
    if not width.isdigit() or not height.isdigit():
        sys.stderr.write("Invalid width or height.")
        return

    # Discard any comments remaining before the image data
    while byte is '#':
        image_file.readline()
        byte = image_file.read(1)

    # Check the last byte before the image data is whitespace
    if byte not in string.whitespace:
        return

    return file_type, (int(width), int(height))


def parse_image(image_file):

    file_type, (width, height) = get_info(image_file)
    dimensions = (width, height)

    if file_type in ['P1', 'P4']:
        mode = '1'
    elif file_type in ['P2', 'P5']:
        mode = 'L'
    else:
        mode = 'RGB'

    image = Image.new(mode, dimensions, 0)

    #P4: need to pad width out to 8:
    row_length = width/8
    if width % 8 is not 0:
        row_length = (width + 8 - width % 8)/8

    contents = image_file.read(row_length*height)

    # Loop through each bit read in and convert it to a byte
    # 0 -> 255, 1 -> 0
    data = ""
    print width
    print height
    for i in range(height):
        for j in range(width):
            position = i * row_length + j/8
            #print position, 7 - j % 8
            if ord(contents[position]) & (1 << 7 - j % 8):
                data += chr(0)
                #sys.stdout.write('X')
            else:
                data += chr(255)
                #sys.stdout.write('.')
        #sys.stdout.write('\n')

    image.putdata(data)



    return image





path = "C:\\Users\\Isabella\\Desktop\\TestPattern 32x32 p4.pbm"
image = open(path, 'rb')
look = parse_image
look(image)




