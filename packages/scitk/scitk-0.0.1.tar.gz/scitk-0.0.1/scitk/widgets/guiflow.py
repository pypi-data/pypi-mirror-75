class Input():# 从文本框，数据库等中输入数据。
    pass

class Drive():# 通过按钮、定时器等东西驱动的事件
    pass

class Process():# 处理过程，其中调用了控件进行设置。
    pass

class View():# 通过画布、表格等内容进行显示。
    pass

class Output(): # 将数据存储到数据库或者文件中。
    pass

class Drive():
    pass

x=r'''
{'type' : 'input',
    'name': 'input_1',
  'source' : 'xls',
  'ports' : { 
                'output' : [{'type':'pandas.DataFrame' , 'name':'output'}],
                'input' : []
                 }
 }
'''
y = r'''
{  'type':'process',
    'name': 'process_1',
    'func':'process_callback',
    'ports':{
                'input':[{'name':'input', 'type':'pandas.DataFrame'}]
                'output': [{'name':'output','type':'pandas.DataFrame'}]
                }
    'control': {(int, 'age', (0,150), 0, 'age', 'years old'),# 参数名是'age'。通过这里就可以获取了。
                    (float, 'h', (0.3, 2.5), 2, 'height', 'm')   # 运行时，首先获取这个字典中对应的值，然后用**kwargs传进去。
                    }
}
'''

if __name__=='__main__':
    d=eval(x)
    print(d)