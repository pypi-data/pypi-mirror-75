from setuptools import setup


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
     name='asexecutor',  
     version='0.2',
     author="Efim Mazhnik",
     author_email="efimmazhnik@gmail.com",
     description="A convenient python library to execute ASE (Atomic Simulation Environment) calculators on clusters.",
     long_description=long_description,
     long_description_content_type="text/x-rst",
     url="https://github.com/efiminem/asexecutor",
     download_url="https://github.com/efiminem/asexecutor/archive/v0.2.zip",
     packages=["asexecutor"],
     package_dir={"asexecutor": "src"},
     install_requires=[
         'ase',
         'paramiko',
     ],
     classifiers=[
         "Development Status :: 2 - Pre-Alpha",
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
