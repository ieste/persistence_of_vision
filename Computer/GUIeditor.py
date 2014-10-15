from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import ImageParser
import math

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
        self.file.add_command(label="New", command = self.new)
        self.file.add_command(label="Open Image", command = self.OpenImage)
        self.file.add_command(label="Save Image", command = self.save_image)
        self.file.add_command(label="Upload")#add command
        self.file.add_command(label="Exit", command = root.destroy)
        self.menu.add_cascade(label="File", menu = self.file)
        root.config(menu=self.menu, padx=5)

        #Toolbar frame
        self.toolbar = Frame(root)
        self.toolbar.grid(row=0, column=0)

        #Canvas
        self.canvas = Canvas(root, bg="light grey", height=200, width=400)
        self.canvas.grid(row=0, column=1)
        
        #Create image on canvas
        self.new()
        
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
        self.width_label = Label(self.select_size, text = 'Resize: ')
        self.width_label.pack(side=LEFT)
        self.width_entry = Entry(self.select_size, width = 10)
        self.width_entry.pack(side=LEFT)
        self.width_entry.bind("<Return>", self.enter_width)

        #Rotated view preview button - in select size frame
        self.preview_button = Button(self.select_size, text = 'Preview', command = self.preview)
        self.preview_button.pack(side=LEFT, padx = 30, ipadx = 30)

        #Set Colour - intialise colour as black
        self.colour = StringVar()
        self.colour = "#000000"
        
        #Colours Frame - in toolbar frame
        self.colours = Frame(self.toolbar)
        self.colours.grid(row=0, column=0, padx=10)

        #Colour Labels - in colours frame
        self.c_select = Label(self.colours, bg = self.colour, relief=RAISED)
        self.c_select.pack(ipadx=12, pady=10)
        self.c1 = Label(self.colours, bg = '#ffffff', relief=SUNKEN)
        self.c1.pack(ipadx=12, pady=2)
        self.c2 = Label(self.colours, bg = '#cccccc', relief=SUNKEN)
        self.c2.pack(ipadx=12, pady=2)
        self.c3 = Label(self.colours, bg = '#999999', relief=SUNKEN)
        self.c3.pack(ipadx=12, pady=2)
        self.c4 = Label(self.colours, bg = '#666666', relief=SUNKEN)
        self.c4.pack(ipadx=12, pady=2)
        self.c5 = Label(self.colours, bg = '#333333', relief=SUNKEN)
        self.c5.pack(ipadx=12, pady=2)
        self.c6 = Label(self.colours, bg = '#000000', relief=SUNKEN)
        self.c6.pack(ipadx=12, pady=2)
        
        # Tools Frame
        self.tools = Frame(self.toolbar)
        self.tools.grid(row=0, column=1, padx=5)
        
        #Tool Buttons - in tools frame
        self.draw = Button(self.tools, text = "Draw")
        self.draw.pack(pady=2, fill=X)
        self.line = Button(self.tools, text = "Line")
        self.line.pack(pady=2, fill=X)
        self.fill = Button(self.tools, text = "Fill")
        self.fill.pack(pady=2, fill=X)
        self.erase  = Button(self.tools, text = "Erase")
        self.erase.pack(pady=2, fill=X)
        self.square = Button(self.tools, text = "Square")
        self.square.pack(pady=2, fill=X)
        
        #Canvas Mouse Bind
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release)

        #Colour Mouse Bind for colour labels
        self.c1.bind("<Button-1>", self.c1_click)
        self.c2.bind("<Button-1>", self.c2_click)
        self.c3.bind("<Button-1>", self.c3_click)
        self.c4.bind("<Button-1>", self.c4_click)
        self.c5.bind("<Button-1>", self.c5_click)
        self.c6.bind("<Button-1>", self.c6_click)

        #Tools Mouse Bind for tool buttons
        self.draw.bind("<Button-1>", self.draw_click)
        self.fill.bind("<Button-1>", self.fill_click)
        self.erase.bind("<Button-1>", self.erase_click)
        self.square.bind("<Button-1>", self.square_click)
        self.line.bind("<Button-1>", self.line_click)

    #The following functions select colours based on the colour label that
    #is clicked
    def c1_click(self, e):
        self.colour = '#ffffff'
        self.c_select.configure(bg='#ffffff')

    def c2_click(self, e):
        self.colour = '#cccccc'
        self.c_select.configure(bg='#cccccc')

    def c3_click(self, e):
        self.colour = '#999999'
        self.c_select.configure(bg='#999999')

    def c4_click(self, e):
        self.colour = '#666666'
        self.c_select.configure(bg='#666666')

    def c5_click(self, e):
        self.colour = '#333333'
        self.c_select.configure(bg='#333333')

    def c6_click(self, e):
        self.colour = '#000000'
        self.c_select.configure(bg='#000000')

    #Binds events to line when line button is pressed
    def line_click(self, e):
        self.canvas.bind("<Button-1>", self.line_start)
        self.canvas.bind("<ButtonRelease-1>", self.line_end)
        self.canvas.bind("<B1-Motion>", self.mouse_motion)

    #Sets the intial coordinates for the line draw function
    def line_start(self, e):
        self.x, self.y = (e.x-((360-self.w)/2)-19, e.y-84)
        
    #Sets the end coordinates for the line draw function
    def line_end(self, e):
        x0,y0 = (self.x, self.y)
        x1,y1 = (e.x-((360-self.w)/2)-19, e.y-84)
        self.d = ImageDraw.Draw(self.img)
        self.d.line([x0, y0, x1, y1], fill=self.colour, width=2)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

    #Probably don't need this function, will probably delete
    def fill_click(self, e):
        self.canvas.bind("<Button-1>", self.draw_fill)

    #To be deleted
    def draw_fill(self, e):
        return 0

    #Binds events to erase when erase button is pressed
    def erase_click(self, e):
        self.canvas.bind("<B1-Motion>", self.draw_erase)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_motion)
        
    #Erase function - draws a white circle of 10 pixel diameter
    def draw_erase(self, e):
        x0,y0 = (e.x-((360-self.w)/2)-19, e.y-84)
        self.d = ImageDraw.Draw(self.img)
        self.d.ellipse([x0 ,y0, x0+10, y0+10], fill = 'white', outline='white')
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

    #To be implemented if time permits    
    def square_click(self, e):
        return 0

    #Binds events to draw when draw button is pressed    
    def draw_click(self, e):
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_draw)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_motion)

    #Initialises draw coordinates, and draws single pixel at point
    def start_draw(self, e):
        self.x0,self.y0 = (e.x-((360-self.w)/2)-19, e.y-84)
        self.d = ImageDraw.Draw(self.img)
        self.d.point((self.x0, self.y0), fill=self.colour)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

    #Establishes start and end coordinates for draw when mouse in motion
    def draw_draw(self, e):
        self.x1,self.y1 = (e.x-((360-self.w)/2)-19, e.y-84)
        self.connect_draw(self.x0, self.y0, self.x1, self.y1)
        self.x0, self.y0 = self.x1, self.y1
        self.d = ImageDraw.Draw(self.img)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

    #Connects the start and end coordinates to create fluid line
    #Updates with new coordinates
    def connect_draw(self, x0, y0, x1, y1):
        self.d = ImageDraw.Draw(self.img)
        self.d.line([x0, y0, x1, y1], fill=self.colour)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)
        self.x0, self.y0 = x1, y1

    #Default state for mouse motion
    def mouse_motion(self, e):
        print (e.x-((360-self.w)/2)-19, e.y-84)

    #Default state for mouse click
    def mouse_click(self, e):
        return 0

    #Default state for mouse release
    def mouse_release(self, e):
        return 0

    #Resizes the image width to number in entry widget
    #Will not resize larger than 360 or smaller than 1 pixel
    def enter_width(self, e):
        self.w = self.width_entry.get()
        if self.w == '':
            return 0
        self.w = int(self.width_entry.get())
        if self.w > 360:
            self.w = 360
        if self.w < 1:
            self.w = 1
        self.img = Image.new('RGB', (self.w, self.h), "white")
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

    #Draws text from entry widget onto image centred
    def preview_text(self, e):
        self.text = self.text_entry.get()
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(self.text)
        
        self.d.text((((self.w/2-((self.text_width)/2)), (self.h/2-(self.text_height)/2))),
                    self.text, fill=self.colour)
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

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
            self.canvas.create_image(200, 100, image=self.t)
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
                i+=1
                f.write('\n')
            f.close()

    #Returns image to blank, 360 pixel wide
    def new(self):
        self.w, self.h = 360, 32
        self.img = Image.new('RGB', (self.w, self.h), "white")
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

root = Tk()
app = POVApp(root)
root.mainloop()
