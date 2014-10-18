from Tkinter import *
import tkFileDialog
import tkColorChooser
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from PIL import ImageFile
import math
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
        self.w, self.h = 360, 32

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
        self.draw = Button(self.toolbar, text="Draw")
        self.draw.pack(pady=2, fill=X)
        self.line = Button(self.toolbar, text="Line")
        self.line.pack(pady=2, fill=X)
        self.clear = Button(self.toolbar, text="Clear")
        self.clear.pack(pady=2, fill=X)
        self.erase = Button(self.toolbar, text="Erase")
        self.erase.pack(pady=2, fill=X)
        self.square = Button(self.toolbar, text="Square")
        self.square.pack(pady=2, fill=X)

        #Tools Mouse Bind for tool buttons
        self.draw.bind("<Button-1>", self.draw_click)
        self.clear.bind("<Button-1>", self.clear_click)
        self.erase.bind("<Button-1>", self.erase_click)
        self.square.bind("<Button-1>", self.square_click)
        self.line.bind("<Button-1>", self.line_click)

        #Canvas
        self.canvas = Canvas(root, bg="light grey", width=400, height=200, highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky=N+W+E+S, padx=(3, 6), pady=6)
        root.columnconfigure(1, weight=1)

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        #Create image on canvas
        self.new()

        #Canvas Mouse Bind
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

        #Text Frame
        self.text = Frame(root)
        self.text.grid(row=1, column=1)
        self.instruct1 = Label(self.text, text='Enter Text: ')
        self.instruct1.pack(side=LEFT)
        self.text_entry = Entry(self.text, width=28)
        self.text_entry.pack(side=LEFT)
        self.text_entry.bind("<Return>", self.preview_text)

        #Select Size Frame
        self.select_size = Frame(root)
        self.select_size.grid(row=2, column=1, pady=5)
        self.width_label = Label(self.select_size, text='Resize: ')
        self.width_label.pack(side=LEFT)
        self.width_entry = Entry(self.select_size, width = 10)
        self.width_entry.pack(side=LEFT)
        self.width_entry.bind("<Return>", self.enter_width)

        #Rotated view preview button - in select size frame
        self.preview_button = Button(self.select_size, text='Preview', command=self.preview)
        self.preview_button.pack(side=LEFT, padx=30, ipadx=30)


    #Returns image to blank, 360 pixel wide
    def new(self):
        self.w, self.h = 360, 32
        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.t = ImageTk.PhotoImage(self.img)
        self.tid = self.canvas.create_image(200, 100, image=self.t)

    #Center the image when the canvas is resized
    def on_canvas_resize(self, e):
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()  # Canvas width & height
        self.cxc, self.cyc = cw/2, ch/2  # Canvas x center & y center
        self.canvas.coords(self.tid, self.cxc, self.cyc)

    #Translate coordinates from the canvas reference to the image reference.
    def translate_coords(self, x, y):
        return x-self.cxc+self.w/2, y-self.cyc+self.h/2

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
        print self.translate_coords(e.x, e.y)

    #Default state for mouse release
    def mouse_release(self, e):
        return 0

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
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Establishes start and end coordinates for draw when mouse in motion
    def draw_motion(self, e):
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill=self.colour)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)
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
        self.t = ImageTk.PhotoImage(temp_img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Sets the end coordinates for the line draw function
    def line_end(self, e):
        x0, y0 = (self.x, self.y)
        x1, y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    ## Clear

    #Clear the image
    def clear_click(self, e):
        self.img = Image.new('RGB', (self.w, self.h), "black")
        self.t = ImageTk.PhotoImage(self.img)
        self.tid = self.canvas.create_image(self.cxc, self.cyc, image=self.t)

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
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    #Establishes start and end coordinates for draw when mouse in motion
    def erase_motion(self, e):
        self.x1, self.y1 = self.translate_coords(e.x, e.y)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([self.x0, self.y0, self.x1, self.y1], fill='black', width=10)
        self.d.ellipse([self.x1-5, self.y1-5, self.x1+5, self.y1+5], fill='black', outline='black')
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)
        self.x0, self.y0 = self.x1, self.y1

    ## Square

    #To be implemented if time permits
    def square_click(self, e):
        return 0

    ## Text

    #Draws text from entry widget onto image centred
    def preview_text(self, e):
        self.text = self.text_entry.get()
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(self.text)
        
        self.d.text((((self.w/2-((self.text_width)/2)), (self.h/2.0-(self.text_height)/2))),
                    self.text, fill=self.colour)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

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
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.tid, image=self.t)

    ## Preview

    #Opens new window with image displayed as would appear on the POV display
    def preview(self):

        #Initialise image data, height and width variables
        self.preview_data = []
        h = 0
        w = 0

        #Open a new window with canvas
        self.rotate_preview = Toplevel()
        self.preview_canvas = Canvas(self.rotate_preview, bg="light grey", width=96, height=96)
        self.preview_canvas.pack()

        #Checks pixel type and puts image data into list
        self.pixel = self.img.getpixel((0, 0))
        if type(self.pixel) == tuple:
            for i in list(self.img.getdata()):
                self.preview_data.append(str(i[0]))
        else:
            for i in list(self.img.getdata()):
                self.preview_data.append(str(i))

        #Setting up image to be drawn
        #Draws blank image, outside radius 96, inner radius 32
        self.preview_image = Image.new('RGB', (96, 96), "#d3d3d3")
        self.pidraw = ImageDraw.Draw(self.preview_image)
        self.pidraw.ellipse([0, 0, 96, 96], fill="white")
        self.pidraw.ellipse([32, 32, 64, 64], fill="#d3d3d3")

        #Reverse mapping maths
        #For rect coords (x, y) in rotated image, find radius d from centre (x=48, y=48)
        #Find angle theta starting from 'negative y' axis (ie from first half y axis)
        #Let r = height in original image
        #Let theta = width in original image
        #Get colour from original image data list and draw point on rotated image

        #Problems so far: cannot divide by y=0 in atan, so range has to start from 1
        #colour is in wrong format (255 = 'red', needs to be white)
        #values of theta are not varying enough
        #only works for full sized images
        #maths probably is not correct
        #need to reevaluate atan for each quadrant and only draw if r < height

        for y in range(0, 96):
            for x in range(0, 96):
                r = 32-(int(math.hypot(x-48, y-48)-16))
                if x < 48 and y < 48:
                    theta = 180 - abs(int(math.degrees(math.atan((float(48-x)/(48-y))))))
                elif x == 48 and y < 48:
                    theta = 180
                elif x < 48 and y == 48:
                    theta = 90
                elif x == 48 and y > 48:
                    theta = 0
                elif x > 48 and y == 48:
                    theta = 270
                elif x < 48 and y > 48:
                    theta = abs(int(math.degrees(math.atan(float((48-x)/(y-48))))))
                elif x > 48 and y < 48:
                    theta = abs(int(math.degrees(math.atan(float(((x-48)/(48-y)))))))+180
                elif x > 48 and y > 48:
                    theta = abs(int(math.degrees(math.atan(float((y-48)/(x-48))))))+270
                if r < 32 and r > 0:

                    #print statement to check values
                    #print ("x:{} y:{} r:{} theta:{}" .format(x, y, r, theta))

                    colour = StringVar()
                    colour = '#%02x%02x%02x' %(int(self.preview_data[self.w*r + theta]),int(self.preview_data[self.w*r + theta]),int(self.preview_data[self.w*r + theta]))
                    self.pidraw.point((x, y), fill=colour)

                    #print ("x:{} y:{} r:{} theta:{} colour:{}" .format(x, y, r, theta, colour))

        self.piphoto = ImageTk.PhotoImage(self.preview_image)
        self.preview_canvas.create_image(48,48, image=self.piphoto)

        """
        #Initialise image data, height and width variables
        self.preview_data = []
        h = 0
        w = 0

        #Open a new window with canvas
        self.rotate_preview = Toplevel()
        self.preview_canvas = Canvas(self.rotate_preview, bg="light grey", width=96, height=96)
        self.preview_canvas.pack()

        #Checks pixel type and puts image data into list
        self.pixel = self.img.getpixel((0,0))        
        if type(self.pixel) == tuple:
            for i in list(self.img.getdata()):
                self.preview_data.append(str(i[0]))
        else:
            for i in list(self.img.getdata()):
                self.preview_data.append(str(i))
                
        #Setting up image to be drawn
        #Draws blank image, outside radius 96, inner radius 32
        self.preview_image = Image.new('RGB', (96, 96), "#d3d3d3")
        self.pidraw = ImageDraw.Draw(self.preview_image)
        self.pidraw.ellipse([0,0,96,96], fill="white")
        self.pidraw.ellipse([32,32,64,64], fill="#d3d3d3")

        #Reverse mapping maths
        #For rect coords (x, y) in rotated image, find radius d from centre (x=48, y=48)
        #Find angle theta starting from 'negative y' axis (ie from first half y axis)
        #Let r = height in original image
        #Let theta = width in original image
        #Get colour from original image data list and draw point on rotated image

        #Problems so far: cannot divide by y=0 in atan, so range has to start from 1
        #colour is in wrong format (255 = 'red', needs to be white)
        #values of theta are not varying enough
        #only works for full sized images
        #maths probably is not correct
        #need to reevaluate atan for each quadrant and only draw if r < height
        
        for y in range(1,96):
            for x in range(1,96):
                r = 32-int(math.hypot(x-48, y-48)-16)
                if x < 48 and y <48:
                    theta = int(math.degrees(math.atan((48-x)/(48-y))))
                elif x < 48 and y > 48:
                    theta = int(math.degrees(math.atan((48-x)/y)))
                elif x > 48 and y <48:
                    theta = int(math.degrees(math.atan((x/(48-y)))))
                elif x > 48 and y > 48:
                    theta = int(math.degrees(math.atan(x/y)))
                if r<32 and theta <360:
                    
                    #print statement to check values
                    #print ("x:{} y:{} r:{} theta:{}" .format(x, y, r, theta))

                    colour = StringVar()
                    colour = int(self.preview_data[self.w*r + theta])
                    self.pidraw.point((x, y), fill=colour)                   

        self.piphoto = ImageTk.PhotoImage(self.preview_image)
        self.preview_canvas.create_image(48,48, image=self.piphoto)
        """


    ## Menu

    #Opens image through Image Parser
    def OpenImage(self):
        self.imagefile = tkFileDialog.askopenfilename()
        try:
            im = open(self.imagefile, 'rb')
            self.img=ImageParser.parse_image(im)
            self.info =  ImageParser.get_info(im)
            self.size = self.info[1]
            self.w = self.size[0]
            self.h = self.size[1]
            self.t = ImageTk.PhotoImage(self.img)
            self.canvas.delete(ALL)
            self.canvas.itemconfig(self.tid, image=self.t)
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
            print "USB Device not found."
            return
        avr.write_pages(ImageParser.image_to_data(self.img))

root = Tk()
app = POVApp(root)
root.mainloop()
