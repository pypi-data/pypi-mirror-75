from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='toolman',
      version='0.1.9',
      description='Python utility tools for research',
      url='https://github.com/bohaohuang/toolman',
      author='bohaohuang',
      author_email='hbhzhuce@gmail.com',
      license='MIT',
      packages=['toolman'],
      long_description=readme(),
      install_requires=[
            'numpy',
            'Pillow',
            'scikit-learn',
            'scikit-image',
            'natsort',
            'matplotlib',
            'torchsummary',
            'pandas',
      ],
      zip_safe=False)
