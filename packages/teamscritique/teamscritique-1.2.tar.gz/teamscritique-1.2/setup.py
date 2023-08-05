from setuptools import setup

setup(name='teamscritique',
      version='1.2',
      description='library for sentiment analysis for Teams call',
      url='https://github.com/rahul24/CritiqueForTeams',
      author='Xiao Yin',
      author_email='yinxiao@microsoft.com',
      license='MIT',
      packages=['teamscritique'],
      install_requires=[
          'librosa==0.8.0',
          'soundfile',
          'numpy==1.19.1',
          'sklearn',
          'pandas',
          'scipy',
          'pathlib',
      ],
      include_package_data=True,
      zip_safe=False)