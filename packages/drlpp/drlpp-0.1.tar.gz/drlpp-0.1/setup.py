from setuptools import setup

setup(name='drlpp',
      version='0.1',
      description='Dynamic Resource Locator Protocol for Python',
      url='http://github.com/yesmyc/drlpp',
      author='ltaoit',
      author_email='ltaoist6@gmail.com',
      license='GPLv3',
      packages=[
          'drlpp',
      ],
      entry_points={
          'console_scripts': [
            'drlpp = drlpp:main',
            ]
      },
      zip_safe=False
)
