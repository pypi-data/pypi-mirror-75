from setuptools import setup

setup(name='teamscritique',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Xiao Yin',
      author_email='yinxiao@microsoft.com',
      license='MIT',
      packages=['teamscritique'],
      install_requires=[
          'librosa',
          'soundfile',
          'numpy',
          'sklearn',
          'pandas',
          'scipy',
      ],
      zip_safe=False)