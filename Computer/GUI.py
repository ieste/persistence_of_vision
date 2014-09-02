from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class POVApp(object):
    """Top level POV Display application"""
    

    def __init__(self, root):
        #Main Window
        root.title('POV Wheel')
        
        #Menu Bar
        self.menu = Menu(root)
        self.file = Menu(root)
        self.file.add_command(label="Exit", command=root.destroy)
        self.menu.add_cascade(label="File", menu=self.file)
        root.config(menu=self.menu)

        #Text Frame
        self.text = Frame(root)
        self.text.pack(expand=True, pady=30, padx=30)

        self.instruct1 = Label(self.text, text='Enter Text: ')
        self.instruct1.grid(row=0)

        self.text_entry = Entry(self.text, width=28)
        self.text_entry.grid(row=0, column=1, sticky=W)

        self.text_buttons = Frame(self.text)
        self.text_buttons.grid(row=1, column=1, pady=10, sticky=W)

        self.upload_text = Button(self.text_buttons, text='Upload',
                                  command=self.upload_text)
        self.upload_text.pack(fill=X, ipadx=30, side=LEFT)
        
        self.preview_text = Button(self.text_buttons, text='Preview',
                                  command=self.preview_text)
        self.preview_text.pack(fill=X, side=LEFT, ipadx=30, padx=17)
        
        #Image Frame
        self.image = Frame(root)
        self.image.pack(expand=True, pady=30, padx=30)

        self.instruct2 = Label(self.image, text='Image: ')
        self.instruct2.grid(row=0)

        self.find_image = Button(self.image, text='Find...', width=27,
                                 command=self.OpenImage)
        self.find_image.grid(row=0, column=1, sticky=W)

        self.image_buttons = Frame(self.image)
        self.image_buttons.grid(row=1, column=1, pady=10, sticky=W)

        self.upload_image = Button(self.image_buttons, text='Upload',
                                  command=self.upload_image)
        self.upload_image.pack(fill=X, ipadx=30, side=LEFT)
        
        self.preview_image = Button(self.image_buttons, text='Preview',
                                  command=self.preview_image)
        self.preview_image.pack(fill=X, side=LEFT, ipadx=30, padx=17)

    
    def upload_text(self):
        return NULL
    
    def preview_text(self):
        self.displaytext = Toplevel()
        
        self.text = self.text_entry.get()
        self.img = Image.new('RGB', (360, 32), "white")
        self.d = ImageDraw.Draw(self.img)
        self.text_width, self.text_height = self.d.textsize(self.text)
        self.d.text((((180-((self.text_width)/2)), (16-(self.text_height)/2))),
                    self.text, fill=("black"))
        self.t = ImageTk.PhotoImage(self.img)
        
        self.canvas1 = Canvas(self.displaytext, width=360, height=32)
        self.canvas1.pack(expand=YES, fill=BOTH)
        self.canvas1.create_image((180,16),image=self.t)

        #img.save("image.png")
        #self.img.show()

    def OpenImage(self):
        self.imagefile = tkFileDialog.askopenfilename()
        self.f=open(self.imagefile, "r")
        self.im=Image.open(self.f)
        #self.im.show()

    def upload_image(self):
        return NULL
    
    def preview_image(self):
        self.displayimage = Toplevel()

        self.i = ImageTk.PhotoImage(self.im)
        
        self.canvas2 = Canvas(self.displayimage, width=360, height=32)
        self.canvas2.pack(expand=YES, fill=BOTH, padx=3, pady=3)
        self.canvas2.create_image((180,16), image=self.i)

root = Tk()
app = POVApp(root)
root.mainloop()
