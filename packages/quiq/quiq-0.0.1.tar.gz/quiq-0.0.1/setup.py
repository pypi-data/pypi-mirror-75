import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quiq",
    version="0.0.1",
    author="Zachary Dingels",
    author_email="dingelsz3@gmail.com",
    description="A simple and lightweight TDD unit testing framework.",
    license="GNU GPL3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dingelsz/quiq",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
