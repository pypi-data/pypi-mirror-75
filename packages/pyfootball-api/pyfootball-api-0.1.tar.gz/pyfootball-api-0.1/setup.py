import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="pyfootball-api",
    version="0.1",
    author="Marco Müllner",
    author_email="muellnermarco@gmail.com",
    description="A wrapper for https://www.api-football.com/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muma7490/SMURFS",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
