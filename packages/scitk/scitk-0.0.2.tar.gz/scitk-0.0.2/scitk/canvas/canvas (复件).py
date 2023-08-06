import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
# Create a window
window = tk.Tk()
window.title("OpenCV and Tkinter")

# Load an image using OpenCV
cv_img2 = cv2.cvtColor(cv2.imread("/home/hzy/Desktop/深度截图_选择区域_20200613232201.png"), cv2.COLOR_BGR2RGB)
cv_img=np.column_stack((cv_img2,cv_img2))
print(cv_img.shape)
 # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
height, width, no_channels = cv_img.shape

class Canvas(tk.Canvas):
    def __init__(self,master,width,height):
        super().__init__(master,width = width, height = height)
        self.images=[]
        self.image=None
        self.imgtmp=None
        self.imgpos=(0,0)
        self.relativePos=(0,0)
        self.bind('<B1-Motion>',self.showImage)
        self.bind('<ButtonRelease-1>',self.endDrag)
        self.bind('<ButtonPress-1>',self.startDrag)
        self.fps=0
        self.t1=self.t0=time.time()
        self.img=cv_img
    def startDrag(self,event):
        self.relativePos=(-event.x+self.imgpos[0],-event.y+self.imgpos[0])
    def endDrag(self,event):
        pass
    def showImage(self,event):
        global cv_img,photo
        self.t1=time.time()
        if self.t1-self.t0>=1:
            print(self.fps)
            self.fps=0
            self.t0=time.time()
        self.imgtmp = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
        self.create_image(event.x+self.relativePos[0],event.y+ self.relativePos[1], image=self.imgtmp, anchor=tk.NW)
        self.fps+=1
        
# Create a canvas that can fit the above image
canvas = Canvas(window, width = width, height = height)
canvas.pack(side=tk.LEFT)
##c2= Canvas(window, width = width, height = height)
##c2.pack(side=tk.LEFT)
# Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage

 
 # Add a PhotoImage to the Canvas

window.mainloop()
