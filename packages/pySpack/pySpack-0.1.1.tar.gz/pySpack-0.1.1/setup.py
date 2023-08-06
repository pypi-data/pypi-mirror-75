import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("../VERSION", "r") as vr:
    version_number = vr.read()

setuptools.setup(
    name="pySpack",
    version=version_number,
    author="Nex Sabre",
    author_email="nexsabre@protonmail.com",
    description="Python wrapper for few Spack's commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NexSabre/pySpack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
