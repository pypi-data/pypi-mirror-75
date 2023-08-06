from setuptools import setup
setup(name='myBestTools',
      version='1.9',
      description='my Tool',
      author='Du HongYu',
      author_email='837058201@qq.com',
      packages=['tools'],
      zip_safe=False,
      install_requires=[
            'pika',
            'requests',
            'lxml',
            'redis',
            'pymysql',
            'wrapt'
      ]
)