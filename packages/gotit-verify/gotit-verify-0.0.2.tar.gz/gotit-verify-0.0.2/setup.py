import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gotit-verify",
    version="0.0.2",
    author="Phi Nguyen",
    author_email="phi@gotitapp.co",
    description="A Verify SDK for confirming identity of GotIt authenticated apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xoxwaw/",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "coverage==5.2.1",
        "marshmallow==3.7.1",
        "PyJWT==1.7.1",
        "pytest==5.4.3",
        "pytest-cov==2.10.0",
        "pytest-mock==3.2.0",
        "python-dotenv==0.14.0",
        "requests==2.24.0",
        "requests-mock==1.8.0"
   ]
)
