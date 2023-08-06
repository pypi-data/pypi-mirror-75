import setuptools

# include additional packages as well - requests , tabulate , json

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyTypeWriter", # Replace with your own username
    version="0.18",
    author="Harsh Native",
    author_email="Harshnative@gmail.com",
    description="This module lets you quickly add type writer sound effect for inputs to your python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshnative/easyTypeWriter_module_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "playsound",
    ]
)