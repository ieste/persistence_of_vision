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
        
        for y in range(0,96):
            for x in range(0,96):
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
                if r<32 and r>0:
                    
                    #print statement to check values
                    #print ("x:{} y:{} r:{} theta:{}" .format(x, y, r, theta))

                    colour = StringVar()
                    colour = '#%02x%02x%02x' %(int(self.preview_data[self.w*r + theta]),int(self.preview_data[self.w*r + theta]),int(self.preview_data[self.w*r + theta]))
                    self.pidraw.point((x, y), fill=colour)

                    #print ("x:{} y:{} r:{} theta:{} colour:{}" .format(x, y, r, theta, colour))

        self.piphoto = ImageTk.PhotoImage(self.preview_image)
        self.preview_canvas.create_image(48,48, image=self.piphoto)
