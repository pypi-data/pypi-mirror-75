from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read() 

classifiers = [
  "Programming Language :: Python :: 2",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent"
]
 
setup(
  name='capuccino',
  version='0.0.1',
  description='Library to help python developers wtih sql server connections',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Silvio Lacerda',
  author_email='silviolacerda21@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='sql server', 
  packages=find_packages(),
  install_requires=['pyodbc', 'pandas'] 
)