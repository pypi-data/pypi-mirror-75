#from distutils.core import setup
from setuptools import setup, find_packages

VERSION = '0.0.3'

tests_require = []

install_requires = []

setup(name='subwaydetec', # 模块名称
      url='https://github.com/No360201/detector',  # 项目包的地址
      author="No.36",  # Pypi用户名称
      author_email='as-69@qq.com',  # Pypi用户的邮箱
      keywords='python django admin autoregister',
      description='Automatically register models in the admin interface in a smart way.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': [] },
      packages=find_packages(),
)