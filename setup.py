from setuptools import setup

with open("README.md", "r", encoding="utf8") as rm:
    readme = rm.read()
    
with open("requirements.txt") as rq:
    requirements = rq.read().split('\n')

setup(
      name="lzhw",
      version="1.0.0", 
      description="Big lists and/or pandas dataframes compression using an optimized algorithm (lzhw) developed from Lempel-Ziv, Huffman and LZ-Welch techniques",
      packages=["lzhw"],
      install_requires=requirements,
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/MNoorFawi/lzhw",
      author="Muhammad N. Fawi",
      author_email="m.noor.fawi@gmail.com",
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
      )
