import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='summarizer-yshi0914',  
     version='0.0.1',
     author="James Shi",
     author_email="yshi0914@gmail.com",
     description="A BERT-based DBSCAN summarizer package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/yshi0914/bert-based-extractive-summarizer",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )