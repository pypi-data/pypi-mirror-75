from setuptools import setup
setup(name='X30',
      version='5.2.30',
      author='yirutsai',
      author_email='b06502052@ntu.edu.tw',
      packages = ['X30'],
      url = 'https://scott870924.wixsite.com/yirutsai',
      download_url = "https://github.com/yirutsai/X30/archive/5.2.30.tar.gz",
      install_requires=[
                "pygame"
          ],
      entry_points={
          'console_scripts':[
              'test=X30:test',
              #'pill=X30:pill'
          ]
      }
)
