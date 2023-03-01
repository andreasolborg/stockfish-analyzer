# This is a TODO, need to create it and test it so the teacher can easly run our application

from setuptools import setup

setup(
   name='chess-assignment',
   version='1.0',
   description='Analyze chess games',
   author='Andreas Olborg and Jon Grendstad',
   packages=['chess-assignment'],  #same as name
   install_requires=['docx', 'openpyxl'], #external packages as dependencies
)