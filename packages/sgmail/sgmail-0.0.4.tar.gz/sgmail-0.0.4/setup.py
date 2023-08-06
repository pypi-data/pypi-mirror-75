import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgmail",
    version="0.0.4",
    author="Timotheos Savva",
    author_email="timotheos.savva12@gmail.com",
    description="A simple script that sends email with gmail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/timosdvs/sgmail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
