import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qx-rest", 
    version="0.0.1",
    author="Kevin Pulley",
    author_email="kpulley@imaginecommunications.com",
    description="Simple REST interface to the Phabrix Qx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UndyingScroll",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       
   ],
    python_requires='>=3.6',
)
