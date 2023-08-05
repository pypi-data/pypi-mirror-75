# encoding: utf-8
from setuptools import setup, find_packages

pkg = "rosubfix"
ver = "0.0.0"

with open(pkg + "/version.py", "wt") as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(
    name=pkg,
    version=ver,
    description=("Fix diacritics in romanian subtitles"),
    author="Eduard Christian Dumitrescu",
    author_email="eduard.c.dumitrescu@gmail.com",
    license="LGPLv3",
    url="https://hydra.ecd.space/eduard/rosubfix/",
    packages=find_packages(),
    install_requires=["chardet", "cached_property", "attrs"],  # also need PyQt5
    package_data={pkg: ["*.ui"]},
    classifiers=[
        "Environment :: X11 Applications :: Qt",
        "Natural Language :: Romanian",
        "Topic :: Text Processing :: Filters",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={"gui_scripts": ["rosubfix=" + pkg + ".__main__:main"]},
)
