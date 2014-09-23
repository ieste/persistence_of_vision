from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import ImageParser

class POVApp(object):
    """Top level POV Display application"""
    
    def __init__(self, root):
        #Main Window
        root.title('POV Wheel')
        
        #Menu Bar
        self.menu = Menu(root)
        self.file = Menu(root)
        self.file.add_command(label="Open Image", command=self.OpenImage)
        self.file.add_command(label="Save Image")#add command
        self.file.add_command(label="Exit", command=root.destroy)
        self.menu.add_cascade(label="File", menu=self.file)
        root.config(menu=self.menu)

        #Canvas
        self.canvas = Canvas(root, bg="light grey", bd = 3, height=200, width=400)
        self.canvas.pack(expand=True)

        #Create image on canvas
        self.img = Image.new('RGB', (360, 32), "white")
        self.pi = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.pi)
        
        #Text Frame
        self.text = Frame(root)
        self.text.pack(expand=True, pady=20, padx=20)
        
        self.instruct1 = Label(self.text, text='Enter Text: ')
        self.instruct1.pack(side=LEFT)

        self.text_entry = Entry(self.text, width=28)
        self.text_entry.pack(side=LEFT)

        self.preview_text = Button(self.text, text='Preview',
                                  command=self.preview_text)
        self.preview_text.pack(fill=X, side=LEFT, ipadx=30, padx=17)
        
    def preview_text(self):
        self.text = self.text_entry.get()
        #self.img = Image.new('RGB', (360, 32), "white")
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(self.text)
        self.d.text((((180-((self.text_width)/2)), (16-(self.text_height)/2))),
                    self.text, fill=("black"))
        self.t = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.t)

        
    def OpenImage(self):
        self.imagefile = tkFileDialog.askopenfilename()
        #self.f=open(self.imagefile, "r")
        #self.im=Image.open(self.f)
        im = open(self.imagefile, 'rb')
        self.img=ImageParser.parse_image(im)
        #self.im.show()
        
        self.i = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 100, image=self.i)
        
root = Tk()
app = POVApp(root)
root.mainloop()
