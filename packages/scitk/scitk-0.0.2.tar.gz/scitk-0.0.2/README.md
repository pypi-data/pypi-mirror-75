# scitk
split widgets from imagepy to make it could be used independently.

scitk是一个与sciwx接口名称相同的库，只是所使用的库种类与sciwx不同。sciwx基于wxpython而scitk基于tkinter。

相对而言scitk的功能完整度和界面的精美程度不如sciwx，但是scitk的兼容性某些情况下可以较sciwx好一些，也适合使用tkinter快速创建应用。

scitk依赖pyopengltk这个库进行opengl渲染与绘制。

在canvas处依赖PIL。只依赖这些库的话，渲染的帧率有时可以达到80帧左右。

有机会的话需要Image这个类中各种变量含义的文档（入口参数比较多，不太懂如何调用...）



示例

add_view(view_type,view_name) 
view_type有以下几种选项：
	'plot'代表加入绘图选项卡
	'text'加入文本编辑选项卡[TODO]
	'canvas'加入图像画布选项卡[TODO]
add_control(name,widget_type,text)
	name:按钮的名称
	widget_type:控件的类型
	text:控件显示的文字
add_param(name,param_type,arguments,callback,initial_value)

```python
import tkinter as tk
from sciapp import SciApp,run_app
import numpy as np

def func(app):    
    val = app.get_param_widget('value_input').get_value()
    print(val)    

    v = app.get_view_widget('plot_frame')
    fig = v.get_figure(0)# 获取第1个选项卡中的figure。
    fig.clf()
    ax = fig.add_subplot()
    ax.plot(np.linspace(0,1,100),val*np.random.randn(100))
    v.update()

def add_widgets(app:SciApp):
    app.add_view('plot','plot_frame')
    app.add_control('controlbutton',func,'Click me')
    app.add_param('value_slider','slide',( (1, 150), 0, 'weight','kg'),initial_value = 50,callback=lambda:print('hello worldc'))
    app.add_param( 'value_input',float,((0.3, 2.5), 2, 'aa', ''),initial_value=1.72)
    v = app.get_view_widget('plot_frame')
    ax = v.create_subplot()
    
if __name__=='__main__':
    run_app(add_widgets) 
```
注意：最后run_app处，直接传入add_widgets,不能写成add_widgets()