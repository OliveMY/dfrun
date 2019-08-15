from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='dfrun',
      version='0.1.2',
      packages=['dfrun'],
      author="Rudolfxx",
      author_email="mayeoliver@163.com",
      description="Code copier for multi experiments",
      long_description=long_description,
      long_description_content_type="text/markdown",
      entry_points={
          'console_scripts': [
              'dfrun = dfrun.__main__:main'
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
