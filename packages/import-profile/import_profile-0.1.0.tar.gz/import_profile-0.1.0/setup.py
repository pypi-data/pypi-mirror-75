from setuptools import setup, find_packages

pkg = "import_profile"
ver = "0.1.0"

with open(pkg + "/version.py", "wt") as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(
    name=pkg,
    version=ver,
    description=("Profile your imports' CPU and RAM usage"),
    author="Eduard Christian Dumitrescu",
    license="LGPLv3",
    url="https://hydra.ecd.space/eduard/import_profile/",
    packages=find_packages(),
    package_data={},
    install_requires=["psutil"],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
)
