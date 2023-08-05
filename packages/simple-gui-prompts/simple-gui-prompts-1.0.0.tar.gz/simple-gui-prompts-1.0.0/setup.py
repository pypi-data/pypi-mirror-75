import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-gui-prompts",
    version="1.0.0",
    author="Bruce Blore",
    author_email="bruceblore@protonmail.com",
    description="Easily generate GUI prompts without the hassle of making a whole GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/0100001001000010/simple-gui-prompts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pysimplegui']
)
