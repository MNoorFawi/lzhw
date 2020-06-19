from setuptools import setup, Extension

cython_exists = False
try:
    from Cython.Distutils import build_ext
    cython_exists = True
except ImportError:
    from distutils.command.build_ext import build_ext

if cython_exists:
    ext_modules=[
        Extension("lz20c", ["lzhw/lz20c.pyx"]),
        Extension("lzw_c", ["lzhw/lzw_c.pyx"]),
        Extension("lz77c", ["lzhw/lz77c.pyx"])
    ]
else:
    ext_modules = [
        Extension("lz20c", ["lzhw/lz20c.c"]),
        Extension("lzw_c", ["lzhw/lzw_c.c"]),
        Extension("lz77c", ["lzhw/lz77c.c"])
    ]


with open("README.md", "r", encoding="utf8") as rm:
    readme = rm.read()
    
with open("requirements.txt") as rq:
    requirements = rq.read().split('\n')

setup(
      name="lzhw",
      version="1.1.13",
      description="Compression suite for data frames and tabular data files, csv, excel etc.",
      packages=["lzhw"],
      install_requires=requirements,
      long_description=readme,
      include_package_data=True,
      long_description_content_type="text/markdown",
      url="https://github.com/MNoorFawi/lzhw",
      author="Muhammad N. Fawi",
      author_email="m.noor.fawi@gmail.com",
      cmdclass = {"build_ext": build_ext},
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
      ext_modules = ext_modules
)
