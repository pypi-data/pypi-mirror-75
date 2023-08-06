from setuptools import setup
from distutils.core import setup
import os
setup(name='zeptosoft',
      version='0.5',
      description='creating our first package',
      packages=['zeptosoft'],
      author="D.Achuth",
      py_modules=["greenviz"],
      author_email='achuthaiml@gmail.com',
      data_files=[("",["resized one.jpg"])],
      install_requires=["pillow","matplotlib"]
      )
