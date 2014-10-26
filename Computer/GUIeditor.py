

# Import GUI libraries/modules.
from Tkinter import *
import tkFileDialog, tkColorChooser, tkSimpleDialog

# Import image processing libraries/modules.
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile

# Import other useful modules.
import math
import os

# Import our modules
from USBDevice import USBDevice
import ImageParser

ImageFile.LOAD_TRUNCATED_IMAGES = True


class InvalidFile(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class POVApp(object):
    """Top level POV Display application"""

    def __init__(self, root):
        # Main Window
        root.title('POV Wheel')
        root.geometry('+0+0')
        self._root = root

        # Menu Bar for new, open image, save image, upload and exit functions
        self.menu = Menu(root)
        self.file = Menu(self.menu, tearoff=0)
        self.file.add_command(label="New", command=self.new)
        self.file.add_command(label="Open Image", command=self.open_image)
        self.file.add_command(label="Save Image", command=self.save_image)
        self.file.add_command(label="Upload", command=self.upload_image)
        self.file.add_command(label="Exit", command=root.destroy)
        self.menu.add_cascade(label="File", menu=self.file)
        root.config(menu=self.menu)

        # Toolbar frame for tools and colour selection
        self.toolbar = Frame(root)
        self.toolbar.grid(row=0, column=0, padx=(6, 3), pady=6)

        # Set Colour - initialize colour as white
        self.colour = StringVar()
        self.colour = "#FFFFFF"

        # Configuration for colour selector
        self.c_select = Label(self.toolbar, bg=self.colour, relief=RAISED)
        self.c_select.pack(ipadx=12, pady=10)
        self.c_select.bind("<Button-1>", self.c_select_click)

        # Configuration for tool buttons
        self.drag = Button(self.toolbar, text="Drag")
        self.drag.pack(pady=2, fill=X)
        self.zoom = Button(self.toolbar, text="Zoom")
        self.zoom.pack(pady=2, fill=X)
        self.draw = Button(self.toolbar, text="Draw")
        self.draw.pack(pady=2, fill=X)
        self.line = Button(self.toolbar, text="Line")
        self.line.pack(pady=2, fill=X)
        self.square = Button(self.toolbar, text="Square")
        self.square.pack(pady=2, fill=X)
        self.erase = Button(self.toolbar, text="Erase")
        self.erase.pack(pady=2, fill=X)
        self.clear = Button(self.toolbar, text="Clear")
        self.clear.pack(pady=2, fill=X)
        self.resize = Button(self.toolbar, text="Resize")
        self.resize.pack(pady=2, fill=X)
        self.text = Button(self.toolbar, text="Text")
        self.text.pack(pady=2, fill=X)

        # Binds mouse events to tool buttons
        self.drag.bind("<Button-1>", self.drag_click)
        self.zoom.bind("<Button-1>", self.zoom_click)
        self.draw.bind("<Button-1>", self.draw_click)
        self.line.bind("<Button-1>", self.line_click)
        self.square.bind("<Button-1>", self.square_click)
        self.erase.bind("<Button-1>", self.erase_click)
        self.clear.bind("<Button-1>", self.clear_click)
        self.resize.bind("<ButtonRelease-1>", self.resize_click)
        self.text.bind("<ButtonRelease-1>", self.text_click)

        # Configuration for canvas
        self.canvas = Canvas(root, bg="light grey", width=400, height=200, highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky=N+W+E+S, padx=(3, 6), pady=6)
        root.columnconfigure(1, weight=1)
        self.canvas.bind("<Configure>", self.canvas_resize)

        # Bind mouse events to canvas for tool functionality
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

        # Preview Frame for preview display
        self.previewbtn_frame = Frame(root)
        self.previewbtn_frame.grid(row=1, column=1, pady=5)

        # Rotated view preview button
        self.preview_button = Button(self.previewbtn_frame, text='Update Preview', command=self.preview)
        self.preview_button.pack(side=LEFT, padx=15, ipadx=15)

        # Preview canvas displays rotated preview
        self.preview_multiplier = 3  # How many times bigger to show the preview
        self.preview_canvas = Canvas(root, bg="light grey", width=96*self.preview_multiplier,
                                     height=96*self.preview_multiplier)
        self.preview_canvas.grid(row=2, column=1)

        # Status Bar indicates state of software
        self.statusbar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.grid(row=3, column=0, columnspan=2, sticky=E+W+S)
        root.rowconfigure(3, weight=1)
        self.statusbar_clearid = 0

        # Create image on canvas
        self.tid = None
        self.new()

    def statusbar_text(self, text):
        """Takes text from upload_image function and displays message in statusbar"""
        self.statusbar.config(text=text)
        self.statusbar.after_cancel(self.statusbar_clearid)
        self.statusbar_clearid = self.statusbar.after(3000, lambda: self.statusbar.config(text=""))

    def new(self):
        """Returns image to blank"""
        self.w, self.h = self.ask_width(), 32
        self.cxc, self.cyc = self.canvas.winfo_width()/2, self.canvas.winfo_height()/2
        self.offsetx, self.offsety = 0, 0
        self.zoom_level = 1.0
        self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h  # Zoomed height and width

        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.t = ImageTk.PhotoImage(self.img)
        self.tid = self.canvas.create_image(self.cxc+self.offsetx, self.cyc+self.offsety, image=self.t)

    def ask_width(self, initialvalue=360):
        self._root.update()
        width = tkSimpleDialog.askinteger('Width', 'Please enter an image width.',
                    initialvalue=initialvalue, minvalue=1, maxvalue=360)
        if width is None:
            width = initialvalue
        return width

    def canvas_resize(self, e):
        """Centers the image when the canvas is resized"""
        if self.tid is None:
            return
        # Canvas x center & y center
        self.cxc, self.cyc = self.canvas.winfo_width()/2, self.canvas.winfo_height()/2
        self.canvas.coords(self.tid, self.cxc+self.offsetx, self.cyc+self.offsety)
        # Adjust zoom
        self.zoom_level = float(self.canvas.winfo_width() - 100) / self.w
        if self.zoom_level < 1:
            self.zoom_level = 1.0
        if self.zoom_level > 6:
            self.zoom_level = 6.0

        self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h

        self.update_canvas_img()
        self.check_bounds()

    def translate_coords(self, x, y):
        """Translate coordinates from the canvas reference to the image reference"""
        return int((x-self.cxc+self.zw/2-self.offsetx)/self.zoom_level), \
            int((y-self.cyc+self.zh/2-self.offsety)/self.zoom_level)

    def update_canvas_img(self):
        """Updates the image on the canvas from self.img, or the zoomed image"""
        if self.zoom_level > 1:
            self.zoom_img = self.img.resize((int(self.zw), int(self.zh)))
            self.t = ImageTk.PhotoImage(self.zoom_img)
        else:
            self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    def c_select_click(self, e):
        """Show color chooser"""
        crgb, chex = tkColorChooser.askcolor(self.colour)
        if chex is not None:
            self.colour = chex
            self.c_select.configure(bg=chex)

    ## Default mouse states

    def mouse_click(self, e):
        """Default state for mouse click - do nothing"""
        return 0

    def mouse_motion(self, e):
        """Default state for mouse motion"""
        return 0

    def mouse_release(self, e):
        """Default state for mouse release - do nothing"""
        return 0

    ## Drag
    def drag_click(self, e):
        """When drag tool button is pressed, binds canvas mouse events to drag image"""
        self.canvas.bind("<Button-1>", self.drag_start)
        self.canvas.bind("<B1-Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def drag_start(self, e):
        """Sets anchor coordinates for drag function"""
        self.x0, self.y0 = e.x-self.offsetx, e.y-self.offsety

    def drag_motion(self, e):
        """Drags image in sync with mouse motion"""
        self.offsetx, self.offsety = e.x-self.x0, e.y-self.y0
        self.check_bounds()

    def check_bounds(self):
        """Ensures image cannot be dragged/resized outside of canvas area"""
        if self.offsetx + self.zw/2 + self.cxc <= 30:
            self.offsetx = int(30 - self.zw/2 - self.cxc)
        elif self.offsetx - self.zw/2 - self.cxc >= -30:
            self.offsetx = int(self.zw/2 + self.cxc - 30)

        if self.offsety + self.zh/2 + self.cyc <= 16:
            self.offsety = int(16 - self.zh/2 - self.cyc)
        elif self.offsety - self.zh/2 - self.cyc >= -16:
            self.offsety = int(self.zh/2 + self.cyc - 16)

        self.canvas.coords(self.tid, self.cxc+self.offsetx, self.cyc+self.offsety)

    ## Zoom
    def zoom_click(self, e):
        """When zoom tool button is pressed, binds canvas mouse events to zoom"""
        self.canvas.bind("<Button-1>", self.zoom_start)
        self.canvas.bind("<B1-Motion>", self.zoom_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def zoom_start(self, e):
        """Sets anchor coordinates for zoom function"""
        self.x0 = e.x

    def zoom_motion(self, e):
        """Zooms image in sync with mouse motion, limited to minimum zoom level of 1 and maximum zoom level of 6"""
        zoom_delta = e.x - self.x0
        self.x0 = e.x

        self.zoom_level += zoom_delta/25.0
        if self.zoom_level < 1:
            self.zoom_level = 1.0
        if self.zoom_level > 6:
            self.zoom_level = 6.0

        self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h

        self.update_canvas_img()
        self.check_bounds()

    ## Draw

    def draw_click(self, e):
        """Binds events to draw when draw button is pressed"""
        self.canvas.bind("<Button-1>", self.draw_start)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def draw_start(self, e):
        """Initialises draw coordinates, and draws single pixel at point"""
        self.x0, self.y0 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.point((self.x0, self.y0), fill=self.colour)
        self.update_canvas_img()

    def draw_motion(self, e):
        """Establishes start and end coordinates for draw when mouse in motion"""
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill=self.colour)
        self.update_canvas_img()
        self.x0, self.y0 = self.x1, self.y1

    ## Line

    def line_click(self, e):
        """Binds events to line when line button is pressed"""
        self.canvas.bind("<Button-1>", self.line_start)
        self.canvas.bind("<B1-Motion>", self.line_motion)
        self.canvas.bind("<ButtonRelease-1>", self.line_end)

    def line_start(self, e):
        """Sets the initial coordinates for the line draw function"""
        self.x, self.y = self.translate_coords(e.x, e.y)

    def line_motion(self, e):
        """Draws line between line start and current coordinates"""
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        temp_img = self.img.copy()
        self.d = ImageDraw.Draw(temp_img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        if self.zoom_level > 1:
            temp_img = temp_img.resize((int(self.zw), int(self.zh)))
        self.t = ImageTk.PhotoImage(temp_img)
        self.canvas.itemconfig(self.tid, image=self.t)

    def line_end(self, e):
        """Sets the end coordinates for the line draw function"""
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        self.update_canvas_img()

    ## Clear

    def clear_click(self, e):
        """Clears the image and maintains image dimensions when clear button is clicked"""
        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.update_canvas_img()

    ## Erase

    def erase_click(self, e):
        """Binds events to erase when erase button is pressed"""
        self.canvas.bind("<Button-1>", self.erase_start)
        self.canvas.bind("<B1-Motion>", self.erase_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def erase_start(self, e):
        """Initialises draw coordinates, and draws single pixel at point"""
        self.x0, self.y0 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.ellipse([self.x0-5, self.y0-5, self.x0+5, self.y0+5], fill='black', outline='black')
        self.update_canvas_img()

    def erase_motion(self, e):
        """Establishes start and end coordinates for draw when mouse in motion"""
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill='black', width=10)
        self.d.ellipse([self.x1-5, self.y1-5, self.x1+5, self.y1+5], fill='black', outline='black')
        self.update_canvas_img()
        self.x0, self.y0 = self.x1, self.y1

    ## Square

    def square_click(self, e):
        """Binds events to square when square button is pressed"""
        self.canvas.bind("<Button-1>", self.square_start)
        self.canvas.bind("<B1-Motion>", self.square_motion)
        self.canvas.bind("<ButtonRelease-1>", self.square_end)

    def square_start(self, e):
        """Sets the initial coordinates for the square function"""
        self.x, self.y = self.translate_coords(e.x, e.y)

    def square_motion(self, e):
        """Draws square between square start and current coordinates"""
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        temp_img = self.img.copy()
        self.d = ImageDraw.Draw(temp_img)
        self.d.rectangle([x0, y0, x1, y1], fill=self.colour)
        if self.zoom_level > 1:
            temp_img = temp_img.resize((int(self.zw), int(self.zh)))
        self.t = ImageTk.PhotoImage(temp_img)
        self.canvas.itemconfig(self.tid, image=self.t)

    def square_end(self, e):
        """Sets the end coordinates for the square function"""
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.rectangle([x0, y0, x1, y1], fill=self.colour)
        self.update_canvas_img()

    ## Resize

    def resize_click(self, e):
        """Resizes the image width"""
        newwidth = self.ask_width(initialvalue=self.w)
        newimage = Image.new('RGB', (newwidth, self.h), "black")
        newimage.paste(self.img, ((newwidth-self.w)/2, 0))
        self.w, self.zw = newwidth, newwidth * self.zoom_level
        self.img = newimage
        self.update_canvas_img()

    ## Text

    def text_click(self, e):
        """Draws text onto image centred"""
        text = tkSimpleDialog.askstring('Text', 'Please enter the text you wish to display.')
        if text is None:
            return
        font = ImageFont.load(sys.path[0] + '/resources/courB14.pil')
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(text)

        self.d.text((self.w/2-self.text_width+6, self.h/2-self.text_height),
                    text, fill=self.colour, font=font)

        self.update_canvas_img()

    ## Preview

    def preview(self):
        """Opens new window with image displayed as would appear on the POV display"""
        # Define size variables
        inr = 16*self.preview_multiplier  # Inner Radius
        cen = 48*self.preview_multiplier  # Center
        size = 96*self.preview_multiplier  # Size

        # Create a new preview image
        self.preview_image = Image.new('RGB', (size, size), "#d3d3d3")
        pidraw = ImageDraw.Draw(self.preview_image)
        # Convert the image to rgb
        rgb_img = self.img.convert('RGB')

        # Reverse mapping maths
        # For each rect coords (x, y) in rotated image
        # Convert to cartesian coords with origin at (cen, cen)
        # Find radius r from the origin
        # Find angle theta using atan2
        # Let r = height in original image
        # Let theta = width in original image
        # Get colour from original image

        for x in xrange(size):
            for y in xrange(size):
                xc, yc = x-cen, cen-y

                r = int(float(math.hypot(xc, yc) - inr) / self.preview_multiplier)
                if r >= 32 or r < 0:
                    continue

                theta = math.degrees(math.atan2(xc, yc))
                # Rotate so the center is always at the top
                theta = int(theta + 0.5*self.w) % 360

                # theta = theta % self.w #Repeat the pattern around the wheel
                pixel = rgb_img.getpixel((theta, 31-r)) if theta < self.w else '#000'

                pidraw.point((x, y), fill=pixel)

        self.piphoto = ImageTk.PhotoImage(self.preview_image)
        self.preview_canvas.create_image(cen, cen, image=self.piphoto)

    ## Menu

    def open_image(self):
        """Opens image through Image Parser"""
        self.imagefile = tkFileDialog.askopenfilename()
        try:
            im = open(self.imagefile, 'rb')
            self.img = ImageParser.parse_image(im)
            self.info = ImageParser.get_info(im)
            self.size = self.info[1]
            self.w, self.h = self.size[0], self.size[1]
            self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h
            self.update_canvas_img()
        except InvalidFile as e:
            tkMessageBox.showwarning(title="Invalid File",
                                     message=e)

    def save_image(self):
        """Saves image as P2 type .pgm for any given name"""

        self.data = []
        self.pixel = self.img.getpixel((0, 0))

        if type(self.pixel) == tuple:
            for i in list(self.img.getdata()):
                self.data.append(str(i[0]))
        else:
            for i in list(self.img.getdata()):
                self.data.append(str(i))

        self.data = '\n'.join(self.data)

        from tkFileDialog import asksaveasfilename
        self.filename = asksaveasfilename(defaultextension='.pgm')
        if self.filename:
            f = open(self.filename, "w")
            f.write('P2\n')
            f.write('{} {}\n' .format(self.w, self.h))
            f.write('255\n')
            i = 0
            j = 0
            while i < self.h:
                while j < (self.w*(i + 1)):
                    f.write('{} '.format(self.data.split()[j]))
                    j += 1
                i += 1
                f.write('\n')
            f.close()

    def upload_image(self):
        """Uploads image information to avr via ImageParser
        If USB device not found, returns error status to status bar
        """
        avr = USBDevice(view=self)
        avr.write_pages(ImageParser.image_to_data(self.img))

root = Tk()
root.iconbitmap(sys.path[0] + '/resources/icon.ico')
app = POVApp(root)
root.mainloop()
