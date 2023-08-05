import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="venturelab",
    version="0.0.1",
    author="Aryan Thakur",
    author_email="aryan.aparna.thakur@gmail.com",
    description="A Python Lab Experiments And Testing Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://penshellpenos.web.app",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)