from setuptools import setup, find_packages

VERSION = '0.0.1'

tests_require = []

install_requires = []

setup(name='P-MQTT', # 模块名称
      url='https://github.com/Sonicoms/MQTT/blob/master/',  # 项目包的地址
      author="Sonicom",  # Pypi用户名称
      author_email='1030973627@qq.com',  # Pypi用户的邮箱
      keywords='python P-MQTT admin autoregister',
      description='Automatically register models in the admin interface in a smart way.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
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
