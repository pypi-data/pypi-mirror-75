import setuptools


with open("README.rst", encoding="utf-8") as readme:
    long_description = readme.read()

# The init_file containing the dunder variables __version__,
# __author__ and __contact__.
with open("molgemtools/__init__.py", encoding="utf-8") as init_file:
    exec(init_file.read())

description = "Tools for working with molecular geometry data."
url = "https://gitlab.com/d_attila/molgemtools.git"
documentation = "https://d_attila.gitlab.io/molgemtools/"
source_code = "https://gitlab.com/d_attila/molgemtools.git"

setuptools.setup(name="molgemtools",
                 version=__version__,
                 author=__author__,
                 author_email=__contact__,
                 description=description,
                 long_description=long_description,
                 url=url,
                 project_urls={"Documentation": documentation,
                               "Source Code": source_code},
                 keywords=["computational chemistry",
                           "molecular geometry",
                           "molecular shape matching",
                           "Z-matrix",
                           "Cartesian coordinates"],
                 platforms=["any"],
                 packages=setuptools.find_packages(),
                 license="MIT",
                 package_data={"": ["data/*",
                                    "data/alanine/*",
                                    "data/alanine/conformers/*"]},
                 classifiers=["Programming Language :: Python :: 3",
                              "Operating System :: OS Independent"],
                 python_requires= ">=3.6",
                 setup_requires=["numpy"],
                 install_requires=["numpy"])
