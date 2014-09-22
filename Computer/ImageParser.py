import os.path
import string
import sys
from PIL import Image, ImageDraw


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

    # Return if there is no whitespace separating the dimensions from the type
    if image_file.read(1) not in string.whitespace:
        sys.stderr.write("Whitespace missing between type and dimensions.\n")
        return

    width, height, max_val = "", "", ""
    finished = 0

    # Read in dimensions and max value, discarding comments
    while not finished:
        byte = image_file.read(1)

        if byte is '#':
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
                height = byte
                byte = image_file.read(1)
                while byte not in string.whitespace:
                    height += byte
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

    return file_type, (int(width), int(height)), max_val


def P4_parser(image_file):

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


def P1_parser(image_file):

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


def P2_parser(image_file):

    t, (width, height), max_val = get_info(image_file)
    dimensions = (width, height)

    image = Image.new("RGB", dimensions, "white")

    return image


def parse_image(image_file):

    file_type = get_info(image_file)[0]

    parser = globals().get(file_type + "_parser")

    if not parser:
        sys.stderr.write("Parser for " + file_type + " not found.")
        return

    return parser(image_file)





