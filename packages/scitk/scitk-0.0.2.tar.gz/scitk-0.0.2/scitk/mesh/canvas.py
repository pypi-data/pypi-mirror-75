import time
import tkinter
import numpy as np
from OpenGL import GL
from OpenGL import GLU
from pyopengltk import OpenGLFrame

def circle(x, y, r, n):
    r=abs(r)
    print(r)
    
    theta = np.linspace(0, 2*np.pi, n)
    x = x + r * np.cos(theta)
    y = y + r * np.sin(theta)
    return x, y
class Canvas3D(OpenGLFrame):
    def __init__(self,master,width=200,height=200):
        super(). __init__(master,width=width,height=height)
        self.run=True
    def initgl(self):
        
        """Initalize gl states when the frame is created"""
        GL.glViewport(0, 0, self.width, self.height)
        
        #GL.glClearColor(0.0, 1.0, 0.0, 0.0)    
        self.start = time.time()
        self.nframes = 0
        GLU.gluOrtho2D(-5.0, 5.0, -5.0, 5.0)    # 设置显示范围

    def redraw(self):
        """Render a single frame"""
        if self.run==True:
            self.draw()
    def draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        GL.glBegin(GL.GL_POINTS)
        
        x, y = circle(0, 0, 2+1.5*np.random.randn(),100)
        GL.glColor3f(1.0, 0.0, 0.0)
        for x_, y_ in zip(x, y):
            GL.glVertex2f(x_, y_)
        GL.glEnd()                             # 此次结束
        GL.glFlush() 
        
        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\n" )
        
    def setData(self):
        pass
    def stopOrGo(self):
        self.run=not self.run

def test():
    global b
    b.config(text='eeeeee')
if __name__ == '__main__':
    root = tkinter.Tk()
    frame=tkinter.Frame(root)
    frame.pack()
    app = Canvas3D(frame, width=200, height=200)
    b=tkinter.Button(text='hahahahaha',command=app.stopOrGo)
    b.pack()
    
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1000 // 100# 这样可以控制刷新速度。
    app.after(1000, app.printContext)
    
    app.mainloop()