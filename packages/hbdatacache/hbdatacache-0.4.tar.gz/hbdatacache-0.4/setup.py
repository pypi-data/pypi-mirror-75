import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='hbdatacache',  
     version='0.4',
     #scripts=['hbdatacache.py'] ,
     author="José Henrique Luckmann",
     author_email="joseh.luckmann@gmail.com",
     description="Package to manage temporary files in the cache and streamline codes with downloads and repetitive functions",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ZehLuckmann/hbdatacache",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )