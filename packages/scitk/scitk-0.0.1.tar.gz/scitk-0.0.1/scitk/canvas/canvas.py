import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
from sciapp.action import Tool, DefaultTool
from scitk.canvas.boxutil import cross, multiply, merge, lay, mat, like
from time import time
from scitk.canvas.imutil import mix_img

class Canvas(tk.Canvas):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
    def __init__(self,parent,autofit=False, ingrade=False, up=False):
        super().__init__(parent)
#        self.image=None
##        self.imgtmp=None
##        self.imgpos=(0,0)

        self.winbox = [0,0,300,300] # 窗口
        self.conbox = [0,0,1,1]
        self.oribox = [0,0,1,1]
        
        self.outbak = None
        self.outimg = None
        self.outrgb = None
        self.outbmp = None
        self.outint = None
        self.buffer = None

        self.first = True

        self.images = []
        self.marks = {}
        self.tool = None
        
        self.scaidx = 6
        self.autofit = autofit
        self.ingrade = ingrade
        self.up = up
        self.scrbox = (parent.winfo_screenwidth(),parent.winfo_screenheight())# 屏幕大小

        self.fps=0
        self.t1=self.t0=time()
        self.bindEvents()
        
### 以下为测试代码之后要删去
        self.tool=DefaultTool()
        
        self.imageShownList=[]# tkinter 需要对画布上的对象保持引用才能显示。否则是不会显示的。

    def draw_rgb(self, image, x, y):
        self.imgtmp = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(image))
        self.create_image(x ,y ,image=self.imgtmp, anchor=tk.NW)
        
    def get_obj_tol(self):return self,Tool.default
        
        
    def bindEvents(self):
         self.bind('<Configure>', self.on_size)
         self.bind('<MouseWheel>',self.on_mouse_wheel)
         self.bind('<ButtonPress>',self.on_mouse_down)
         self.bind('<ButtonRelease>',self.on_mouse_up)
         self.bind('<B1-Motion>',self.on_mouse_drag)
    
    def _get_btn_and_others(self,event):# 获取点击鼠标时候按键的输入。
        px, py = event.x, event.y
        self._keydic={17:[False,False,True], 20:[False,True,False], 
                      4:[False,True,True],16:[False]*3,
                    272:[False]*3,276:[False,True,False],273:[False,False,True]
                    ,277:[False,True,True]}
        if event.state in self._keydic.keys(): sta = self._keydic[event.state]
        else: sta=[False]*3
        others = {'alt':sta[0], 'ctrl':sta[1], 'shift':sta[2], 'px':px, 'py':py, 'canvas':self}
        return event.num,others
        
    def on_mouse_move(self,event):
        ename=event.type._name_.lower()
        key,btn=self._get_btn_and_key(event)
        pass
        
    def on_mouse_up(self,event):
        x,y=self.to_data_coor(event.x, event.y)
        btn,others=self._get_btn_and_others(event)
        self.tool.mouse_up(self,  x,  y, btn, **others)    
        self.update()

    def on_mouse_drag(self,event):
        x,y=self.to_data_coor(event.x, event.y)
        btn,others=self._get_btn_and_others(event)
        self.tool.mouse_move(self, x, y, btn, **others)
        self.update()
        
    def on_mouse_down(self,event):
        obj, tol = self.get_obj_tol()
        x,y=self.to_data_coor(event.x, event.y)
        btn,others=self._get_btn_and_others(event)
        self.tool.mouse_down(self, x, y, btn, **others)
        self.update()
        
    def on_mouse_wheel(self,event):
        if event.data<0:
            wheel=-1
        else:
            wheel=1
        x,y=self.to_data_coor(px, py)
        btn,others=self._get_btn_and_others(event)
        self.tool.mouse_wheel(self, x, y, wheel, **others)
             
    def fit(self):
        self.update_box()
        oriw = self.oribox[2]-self.oribox[0]
        orih = self.oribox[3]-self.oribox[1]
        if not self.autofit: a,b,c,d = self.winbox
        else: 
            (a,b),(c,d) = (0,0), self.scrbox
            c, d = c*0.9, d*0.9
        if not self.ingrade:
            for i in self.scales[6::-1]:
                if oriw*i<c-a and orih*i<d-b: break
            self.scaidx = self.scales.index(i)
        else: i = min((c-a)*0.9/oriw, (d-b)*0.9/orih)
        self.zoom(i, 0, 0)
        lay(self.winbox, self.conbox)
        self.update()
        
    def draw_image(self, img, back, mode):
        out, bak, rgb = self.outimg, self.outbak, self.outrgb
        ori, cont = self.oribox, self.conbox
        cellbox = like(ori, cont, img.box)
        csbox = cross(self.winbox, cellbox)#取交叠部分【x1,y1,x2,y2】
        
        if min(csbox[2]-csbox[0], csbox[3]-csbox[1])<5: return
        shp = csbox[3]-csbox[1], csbox[2]-csbox[0]# 交叠部分的形状。
        o, m = mat(self.oribox, self.conbox, cellbox, csbox)# oribox是一个和旋转有关的量，conbox是承载图像的box
        # csbox是上面两个box重叠的部分，也是真正的绘图画布box。 winbox是盛放整个画布窗口的box。
        shp = tuple(np.array(shp).round().astype(np.int))
        
##        print('winbox',self.winbox)
##        print('conbox',self.conbox)
##        print('csbox',csbox,)
       
        if out is None or (out.shape, out.dtype) != (shp, img.dtype):
            self.outimg = np.zeros(shp, dtype=img.dtype)
        if not back is None and not back.img is None and (
            bak is None or (bak.shape, bak.dtype) != (shp, back.dtype)):
            self.outbak = np.zeros(shp, dtype=back.dtype)
        if rgb is None or rgb.shape[:2] != shp:
            self.outrgb = np.zeros(shp+(3,), dtype=np.uint8)
            self.outint = np.zeros(shp, dtype=np.uint8)
        if not back is None:
            mix_img(back.img, m, o, shp, self.outbak, 
                self.outrgb, self.outint, back.rg, back.lut,
                back.log, cns=back.cn, mode='set')
        
        mix_img(img.img, m, o, shp, self.outimg,
            self.outrgb, self.outint, img.rg, img.lut,
            img.log, cns=img.cn, mode=img.mode)
        self.draw_rgb(self.outrgb, *csbox[:2])
        
    def _update(self):
        super().update()
        
    def update(self, counter = [0,0]):
        self.update_box()
        if None in [self.winbox, self.conbox]: return
        if self.first:
            self.first = False
            return self.fit()
        counter[0] += 1
        start = time()
        
        for i in self.images: 
            self.draw_image(i, i.back, 0)
        
        counter[1] += time()-start
        if counter[0] == 50:
            print('frame rate:',int(50/max(0.001,counter[1])))
            counter[0] = counter[1] = 0

    def set_tool(self, tool:Tool):
        self.tool = tool
        
    def update_box(self):
        box = [1e10, 1e10, -1e10, -1e10]
        for i in self.images: box = merge(box, i.box)
        for i in self.marks.values(): box = merge(box, i.box)
        if box[2]<=box[0]: box[0], box[2] = box[0]-1e-3, box[2]+1e-3
        if box[1]<=box[3]: box[1], box[3] = box[1]-1e-3, box[3]+1e-3
        if self.winbox and self.oribox == box: return
        self.conbox = self.oribox = box   

        
    @property
    def scale(self):
        conw = self.conbox[2]-self.conbox[0]
        oriw = self.oribox[2]-self.oribox[0]
        conh = self.conbox[3]-self.conbox[1]
        orih = self.oribox[3]-self.oribox[1]
        l1, l2 = conw**2+conh**2, oriw**2+orih**2
        return l1**0.5 / l2**0.5


    def to_data_coor(self, x, y):
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        x, y = x / self.scale, y / self.scale
        x += -self.conbox[0]/self.scale+self.oribox[0]
        y += -self.conbox[1]/self.scale+self.oribox[1]
        return x, y
        
    def to_panel_coor(self, x, y):
        x, y = x * self.scale, y * self.scale
        x += -self.oribox[0] * self.scale + self.conbox[0]
        y += -self.oribox[1] * self.scale + self.conbox[1]
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        return x, y
                
    def on_paint(self, event):
        if self.buffer is None: return
        wx.BufferedPaintDC(self, self.buffer)
        
    def center(self, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        dx = (self.winbox[2]-self.winbox[0])/2 - x
        dy = (self.winbox[3]-self.winbox[1])/2 - y
        for i,j in zip((0,1,2,3),(dx,dy,dx,dy)):
            self.conbox[i] += j
        lay(self.winbox, self.conbox)
    
    def move(self, dx, dy, coord='win'):
        if coord=='data':
            dx,dy = dx*self.scale, dy*self.scale
        arr = np.array(self.conbox)
        arr = arr.reshape((2,2))+(dx, dy)
        self.conbox = arr.ravel().tolist()
        self.update()
        
    def zoom(self, k, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
            if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        box = np.array(self.conbox).reshape((2,2))
        box = (box - (x,y)) / self.scale * k + (x, y)
        self.conbox = box.ravel().tolist()
        if not self.autofit: return
        a,b,c,d = self.conbox
        if c-a<self.scrbox[0]*0.9 and d-b<self.scrbox[1]*0.9:
            print((c-a+4, d-b+4))
            self.config(width=c-a+4,height=d-b+4)#SetInitialSize((c-a+4, d-b+4))
        lay(self.winbox, self.conbox)
        #self.GetParent().Fit()
        
    def zoomout(self, x, y, coord='win', grade=True):
        if not self.ingrade:
            self.scaidx = min(self.scaidx + 1, len(self.scales)-1)
            i = self.scales[self.scaidx]
        else: i = self.scale * 1.5
        self.zoom(i, x, y, coord)
        self.update()

    def zoomin(self, x, y, coord='win'):
        if not self.ingrade:
            self.scaidx = max(self.scaidx - 1, 0)
            i = self.scales[self.scaidx]
        else: i = self.scale / 1.5
        self.zoom(i, x, y, coord)
        self.update()
        
    def on_size(self, event):
##        if max(self.GetClientSize())>20:
##            self.initBuffer()
        if len(self.images)+len(self.marks)==0: return
        
        self.winbox[2] = self.winfo_width()
        self.winbox[3] = self.winfo_height()
        self.update()
        
    def __del__(self):
        print('========== canvas del')
if __name__=='__main__':
# Create a window
    from sciapp.object import Image
    window = tk.Tk()
    window.title("OpenCV and Tkinter")

    # Load an image using OpenCV
    cv_img2 = cv2.cvtColor(cv2.imread("/home/hzy/Desktop/深度截图_选择区域_20200613232201.png"), cv2.COLOR_BGR2RGB)

     # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
    # Create a canvas that can fit the above image
    canvas = Canvas(window)
    canvas.pack(side=tk.LEFT)
    image = Image()
    image.img = cv_img2
    image.pos = (100,200)
    image.cn = (0,1,2)
    canvas.images.append(image)
    ##c2= Canvas(window, width = width, height = height)
    ##c2.pack(side=tk.LEFT)
    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage

     
     # Add a PhotoImage to the Canvas

    window.mainloop()
