from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='dfrun',
      version='0.1.4',
      packages=['dfrun'],
      author="Rudolfxx",
      author_email="mayeoliver@163.com",
      description="Code copier for multi experiments",
      long_description=long_description,
      long_description_content_type="text/markdown; charset=UTF-8; variant=CommonMark",
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
