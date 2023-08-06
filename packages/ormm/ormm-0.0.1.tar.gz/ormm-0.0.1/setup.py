from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name = "ormm",
    version = "0.0.1",
    description = "Operations Research Models & Methods",
    url = "https://github.com/egbuck/ormm",
    author = "Ethan Buck",
    author_email = "egbuck96@gmail.com",
    packages = find_packages(include=["ormm", "ormm.*"]),
    long_description = long_description,
    long_description_content_type = "text/x-rst",
    install_requires = [
        "pyomo >= 5.0",
    ],
    extras_require = {
        "dev": [
            "pytest >= 6.0",
            "sphinx >= 3.1.2",
            "sphinx_rtd_theme >= 0.5.0",
            "numpydoc >= 1.1.0",
            "twine >= 3.2.0",
            #"check-manifest>=0.42" # used for creating Manifest.in
        ]
    },
    classifiers = [
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)