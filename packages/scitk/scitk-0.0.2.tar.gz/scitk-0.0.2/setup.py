from setuptools import setup,find_packages
setup(name='scitk',
      version='0.0.2',
      description='python GUI framework like sciwx,  based on tkinter, pillow(PIL) and various of functional libs',
      url='https://gitee.com/hzy15610046011/scitk',
      author='Zhanyi Hou',
      author_email='3120388018@qq.com',
      license='MuLan2.0',
      packages=find_packages(),
      include_package_data = True,
      install_requires = ['pillow']
      )#package_data={'':['hat.png']})
     # zip_safe=False,install_requires = ['pyqt5','pyqtgraph','numpy','pyopengl'])
