from Tkinter import *
import tkFileDialog
import tkColorChooser, tkSimpleDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from PIL import ImageFile
import math
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

import ImageParser
from USBDevice import USBDevice


class InvalidFile(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class POVApp(object):
    """Top level POV Display application"""

    def __init__(self, root):
        #Main Window
        root.title('POV Wheel')
        self._root = root

        #Menu Bar
        self.menu = Menu(root)
        self.file = Menu(self.menu, tearoff=0)
        self.file.add_command(label="New", command=self.new)
        self.file.add_command(label="Open Image", command=self.OpenImage)
        self.file.add_command(label="Save Image", command=self.save_image)
        self.file.add_command(label="Upload", command=self.upload_image)
        self.file.add_command(label="Exit", command=root.destroy)
        self.menu.add_cascade(label="File", menu=self.file)
        root.config(menu=self.menu)

        #Toolbar frame
        self.toolbar = Frame(root)
        self.toolbar.grid(row=0, column=0, padx=(6, 3), pady=6)

        #Set Colour - initialize colour as white
        self.colour = StringVar()
        self.colour = "#FFFFFF"

        self.c_select = Label(self.toolbar, bg=self.colour, relief=RAISED)
        self.c_select.pack(ipadx=12, pady=10)
        self.c_select.bind("<Button-1>", self.c_select_click)

        #Tool Buttons

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

        #Tools Mouse Bind for tool buttons
        self.drag.bind("<Button-1>", self.drag_click)
        self.zoom.bind("<Button-1>", self.zoom_click)
        self.draw.bind("<Button-1>", self.draw_click)
        self.line.bind("<Button-1>", self.line_click)
        self.square.bind("<Button-1>", self.square_click)
        self.erase.bind("<Button-1>", self.erase_click)
        self.clear.bind("<Button-1>", self.clear_click)

        #Canvas
        self.canvas = Canvas(root, bg="light grey", width=400, height=200, highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky=N+W+E+S, padx=(3, 6), pady=6)
        root.columnconfigure(1, weight=1)

        self.canvas.bind("<Configure>", self.canvas_resize)

        #Create image on canvas
        self.new()

        #Canvas Mouse Bind
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

        #Input Frame
        self.input_frame = Frame(root)
        self.input_frame.grid(row=1, column=1)


        self.width_label = Label(self.input_frame, text='Resize: ')
        self.width_label.pack(side=LEFT)
        self.width_entry = Entry(self.input_frame, width = 10)
        self.width_entry.pack(side=LEFT, padx=(0,25))
        self.width_entry.bind("<Return>", self.enter_width)

        self.instruct1 = Label(self.input_frame, text='Enter Text: ')
        self.instruct1.pack(side=LEFT)
        self.text_entry = Entry(self.input_frame, width=28)
        self.text_entry.pack(side=LEFT)
        self.text_entry.bind("<Return>", self.preview_text)

        #Preview Frame
        self.previewbtn_frame = Frame(root)
        self.previewbtn_frame.grid(row=2, column=1, pady=5)

        #Rotated view preview button
        self.preview_button = Button(self.previewbtn_frame, text='Update Preview', command=self.preview)
        self.preview_button.pack(side=LEFT, padx=15, ipadx=15)

        #Preview canvas
        self.preview_multiplier = 3 #How many times bigger to show the preview
        self.preview_canvas = Canvas(root, bg="light grey", width=96*self.preview_multiplier, height=96*self.preview_multiplier)
        self.preview_canvas.grid(row=3, column=1)

        #Status Bar
        self.statusbar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.grid(row=4, column=0, columnspan=2, sticky=E+W+S)
        root.rowconfigure(4, weight=1)
        self.statusbar_clearid = 0

    #Display a message on the statusbar
    def statusbar_text(self, text):
        self.statusbar.config(text=text)
        self.statusbar.after_cancel(self.statusbar_clearid)
        self.statusbar_clearid = self.statusbar.after(3000, lambda: self.statusbar.config(text=""))

    #Returns image to blank
    def new(self):
        self.w, self.h = 360, 32
        self.cxc, self.cyc = self.canvas.winfo_width()/2, self.canvas.winfo_height()/2
        self.offsetx, self.offsety = 0, 0
        self.zoom_level = 1.0
        self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h #Zoomed height and width

        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.t = ImageTk.PhotoImage(self.img)
        self.tid = self.canvas.create_image(self.cxc+self.offsetx, self.cyc+self.offsety, image=self.t)

    #Center the image when the canvas is resized
    def canvas_resize(self, e):
        # Canvas x center & y center
        self.cxc, self.cyc = self.canvas.winfo_width()/2, self.canvas.winfo_height()/2
        self.canvas.coords(self.tid, self.cxc+self.offsetx, self.cyc+self.offsety)

    #Translate coordinates from the canvas reference to the image reference.
    def translate_coords(self, x, y):
        return int((x-self.cxc+self.zw/2-self.offsetx)/self.zoom_level), int((y-self.cyc+self.zh/2-self.offsety)/self.zoom_level)

    #Updates the image on the canvas from self.img, or the zoomed image
    def update_canvas_img(self):
        if self.zoom_level > 1:
            self.zoom_img = self.img.resize((int(self.zw), int(self.zh)))
            self.t = ImageTk.PhotoImage(self.zoom_img)
        else:
            self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Show color chooser
    def c_select_click(self, e):
        crgb, chex = tkColorChooser.askcolor(self.colour)
        if chex is not None:
            self.colour = chex
            self.c_select.configure(bg=chex)

    ## Default

    #Default state for mouse click
    def mouse_click(self, e):
        return 0

    #Default state for mouse motion
    def mouse_motion(self, e):
        #print self.translate_coords(e.x, e.y)
        return 0

    #Default state for mouse release
    def mouse_release(self, e):
        return 0

    ## Drag
    def drag_click(self, e):
        self.canvas.bind("<Button-1>", self.drag_start)
        self.canvas.bind("<B1-Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def drag_start(self, e):
        self.x0, self.y0 = e.x-self.offsetx, e.y-self.offsety

    def drag_motion(self, e):
        self.offsetx, self.offsety = e.x-self.x0, e.y-self.y0
        self.check_bounds()

    def check_bounds(self):
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
        self.canvas.bind("<Button-1>", self.zoom_start)
        self.canvas.bind("<B1-Motion>", self.zoom_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    def zoom_start(self, e):
        self.x0 = e.x

    def zoom_motion(self, e):
        zoom_delta = e.x - self.x0
        self.zoom_level += zoom_delta/25.0
        self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h
        self.x0 = e.x

        if self.zoom_level < 1:
            self.zoom_level = 1.0
        if self.zoom_level > 6:
            self.zoom_level = 6.0

        self.update_canvas_img()
        self.check_bounds()

    ## Draw

    #Binds events to draw when draw button is pressed
    def draw_click(self, e):
        self.canvas.bind("<Button-1>", self.draw_start)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    #Initialises draw coordinates, and draws single pixel at point
    def draw_start(self, e):
        self.x0, self.y0 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.point((self.x0, self.y0), fill=self.colour)
        self.update_canvas_img()

    #Establishes start and end coordinates for draw when mouse in motion
    def draw_motion(self, e):
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill=self.colour)
        self.update_canvas_img()
        self.x0, self.y0 = self.x1, self.y1

    ## Line

    #Binds events to line when line button is pressed
    def line_click(self, e):
        self.canvas.bind("<Button-1>", self.line_start)
        self.canvas.bind("<B1-Motion>", self.line_motion)
        self.canvas.bind("<ButtonRelease-1>", self.line_end)

    #Sets the initial coordinates for the line draw function
    def line_start(self, e):
        self.x, self.y = self.translate_coords(e.x, e.y)

    def line_motion(self, e):
        x0,y0 = (self.x, self.y)
        x1,y1 = self.translate_coords(e.x, e.y)
        temp_img = self.img.copy()
        self.d = ImageDraw.Draw(temp_img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        if self.zoom_level > 1:
            temp_img = temp_img.resize((int(self.zw), int(self.zh)))
        self.t = ImageTk.PhotoImage(temp_img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Sets the end coordinates for the line draw function
    def line_end(self, e):
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        self.update_canvas_img()

    ## Clear

    #Clear the image
    def clear_click(self, e):
        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.update_canvas_img()

    ## Erase

    #Binds events to erase when erase button is pressed
    def erase_click(self, e):
        self.canvas.bind("<Button-1>", self.erase_start)
        self.canvas.bind("<B1-Motion>", self.erase_motion)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

    #Initialises draw coordinates, and draws single pixel at point
    def erase_start(self, e):
        self.x0,self.y0 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.ellipse([self.x0-5, self.y0-5, self.x0+5, self.y0+5], fill='black', outline='black')
        self.update_canvas_img()

    #Establishes start and end coordinates for draw when mouse in motion
    def erase_motion(self, e):
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill='black', width=10)
        self.d.ellipse([self.x1-5, self.y1-5, self.x1+5, self.y1+5], fill='black', outline='black')
        self.update_canvas_img()
        self.x0, self.y0 = self.x1, self.y1

    ## Square

    #Binds events to square when square button is pressed
    def square_click(self, e):
        self.canvas.bind("<Button-1>", self.square_start)
        self.canvas.bind("<B1-Motion>", self.square_motion)
        self.canvas.bind("<ButtonRelease-1>", self.square_end)

    #Sets the initial coordinates for the square function
    def square_start(self, e):
        self.x, self.y = self.translate_coords(e.x, e.y)

    def square_motion(self, e):
        x0,y0 = (self.x, self.y)
        x1,y1 = self.translate_coords(e.x, e.y)
        temp_img = self.img.copy()
        self.d = ImageDraw.Draw(temp_img)
        self.d.rectangle([x0, y0, x1, y1], fill=self.colour)
        if self.zoom_level > 1:
            temp_img = temp_img.resize((int(self.zw), int(self.zh)))
        self.t = ImageTk.PhotoImage(temp_img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Sets the end coordinates for the square function
    def square_end(self, e):
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.rectangle([x0, y0, x1, y1], fill=self.colour)
        self.update_canvas_img()

    ## Text

    #Draws text from entry widget onto image centred
    def preview_text(self, e):
        font = ImageFont.load(os.path.dirname(__file__) + '/pilfonts/courB14.pil')
        self.text = self.text_entry.get()
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(self.text)

        self.d.text((self.w/2-self.text_width+6, self.h/2-self.text_height),
                    self.text, fill=self.colour, font=font)

        #Update the image instead of creating a new one,
        #required so that we can resize/zoom the canvas.
        self.update_canvas_img()

    ## Resize

    #Resizes the image width to number in entry widget
    #Will not resize larger than 360 or smaller than 1 pixel
    def enter_width(self, e):
        oldw = self.w
        self.w = self.width_entry.get()
        if self.w == '':
            return 0
        self.w = int(self.width_entry.get())
        if self.w > 360:
            self.w = 360
        if self.w < 1:
            self.w = 1
        oldimg = self.img
        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.img.paste(oldimg, ((self.w-oldw)/2, 0))
        self.update_canvas_img()

    ## Preview

    #Opens new window with image displayed as would appear on the POV display
    def preview(self):

        # Define size variables
        inr = 16*self.preview_multiplier # Inner Radius
        cen = 48*self.preview_multiplier # Center
        size = 96*self.preview_multiplier # Size

        #Create a new preview image
        self.preview_image = Image.new('RGB', (size, size), "#d3d3d3")
        pidraw = ImageDraw.Draw(self.preview_image)
        #Convert the image to rgb
        rgb_img = self.img.convert('RGB')

        #Reverse mapping maths
        #For each rect coords (x, y) in rotated image
        #Convert to cartesian coords with origin at (cen, cen)
        #Find radius r from the origin
        #Find angle theta using atan2
        #Let r = height in original image
        #Let theta = width in original image
        #Get colour from original image

        for x in xrange(size):
            for y in xrange(size):
                xc, yc = x-cen, cen-y

                r = int(float(math.hypot(xc, yc) - inr) / self.preview_multiplier)
                if r >= 32 or r < 0:
                    continue

                theta = math.degrees(math.atan2(xc, yc))
                #Rotate so the center is always at the top
                theta = int(theta + 0.5*self.w)%360

                #theta = theta % self.w #Repeat the pattern around the wheel
                pixel = rgb_img.getpixel((theta, 31-r)) if theta < self.w else '#000'

                pidraw.point((x, y), fill=pixel)

        self.piphoto = ImageTk.PhotoImage(self.preview_image)
        self.preview_canvas.create_image(cen, cen, image=self.piphoto)

    ## Menu

    #Opens image through Image Parser
    def OpenImage(self):
        self.imagefile = tkFileDialog.askopenfilename()
        try:
            im = open(self.imagefile, 'rb')
            self.img=ImageParser.parse_image(im)
            self.info =  ImageParser.get_info(im)
            self.size = self.info[1]
            self.w, self.h = self.size[0], self.size[1]
            self.zw, self.zh = self.zoom_level*self.w, self.zoom_level*self.h
            self.update_canvas_img()
        except InvalidFile as e:
            tkMessageBox.showwarning(title="Invalid File",
                                     message=e)

    #Saves image as P2 type .pgm for any given name
    def save_image(self):
        self.data = []
        self.pixel = self.img.getpixel((0,0))

        if type(self.pixel) == tuple:
            for i in list(self.img.getdata()):
                self.data.append(str(i[0]))
        else:
            for i in list(self.img.getdata()):
                self.data.append(str(i))

        self.data = '\n'.join(self.data)

        from tkFileDialog import asksaveasfilename
        self.filename=asksaveasfilename(defaultextension = '.pgm')
        if self.filename:
            f=open(self.filename, "w")
            f.write('P2\n')
            f.write('{} {}\n' .format(self.w, self.h))
            f.write('255\n')
            i = 0
            j = 0
            while i<self.h:
                while j<(self.w*(i+1)):
                    f.write('{} '.format(self.data.split()[j]))
                    j+=1
                i += 1
                f.write('\n')
            f.close()

    def upload_image(self):
        try:
            avr = USBDevice()
        except:
            #print "USB Device not found."
            self.statusbar_text("USB Device not found.")
            return
        avr.write_pages(ImageParser.image_to_data(self.img))

root = Tk()
app = POVApp(root)
root.mainloop()
