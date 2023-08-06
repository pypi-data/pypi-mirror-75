import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vodajemokrafn", # Replace with your own username
    version="0.0.1",
    author="Kojofix",
    author_email="kojofix@equalggz.eu",
    description="Haha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://equalggz.eu",
    packages=["vodajemokra","vodajemokra.ext","vodajemokra.ext.commands"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)