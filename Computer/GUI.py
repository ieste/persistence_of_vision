from Tkinter import *

#REFERENCE ALPHABET
ABET = {'A' : [30,33,33,63,33,33,33]}

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
                                  command=self.upload)
        self.upload_text.pack(fill=X, ipadx=30, side=LEFT)
        
        self.preview_text = Button(self.text_buttons, text='Preview') # command)
        self.preview_text.pack(fill=X, side=LEFT, ipadx=30, padx=17)

    def upload(self):
        #Only accepts 1 char 'A'
        self.letter = ABET[self.text_entry.get()]
        print self.text_entry.get()
        for self.line in self.letter:
            print "{:06b}".format(self.line)
        #bin(i) converts i in A to binary number

root = Tk()
app = POVApp(root)
root.mainloop()
