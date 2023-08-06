from os import path
from setuptools import setup, find_packages

pkg = "import_profile"
ver = "0.1.1"
base = path.abspath(path.dirname(__file__))

with open(pkg + "/version.py", "wt") as h:
    h.write('__version__ = "{}"\n'.format(ver))

with open(path.join(base, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=pkg,
    version=ver,
    description=("Profile your imports' CPU and RAM usage"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eduard Christian Dumitrescu",
    author_email="eduard.c.dumitrescu@gmail.com",
    license="LGPLv3",
    url="https://hydra.ecd.space/eduard/import_profile/",
    packages=find_packages(),
    package_data={},
    install_requires=["psutil"],  # you also need pandas
    classifiers=["Programming Language :: Python :: 3 :: Only"],
)
