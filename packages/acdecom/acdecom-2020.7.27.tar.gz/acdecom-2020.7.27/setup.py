import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acdecom", # Replace with your own username
    version="2020.07.27",
    author="Stefan Sack, Royal Institute of Technology, Stockholm, Sweden",
    author_email="ssack@kth.se",
    description="A python module for acoustic wave decomposition in flow ducts",
    url="https://github.com/ssackMWL/acdecom/",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    py_modules=["acdecom"],
    python_requires='>=3.7',
    install_requires=['numpy','scipy']
)