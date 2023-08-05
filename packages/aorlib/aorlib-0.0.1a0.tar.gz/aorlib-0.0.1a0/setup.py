import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="aorlib",
    version="0.0.1a",
    author="Tony Benoy",
    setup_requires=["wheel"],
    python_requires=">=3.7",
    author_email="me@tonybenoy.com",
    description="A python library with the ability to interact with Arch Official Repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonybenoy/aorlib",
    install_requires=["httpx"],
    keywords="Arch Linux AUR Arch Offical Repository pacman paur",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ),
    extras_require={"dev": ["black", "pylint", "isort", "mypy"]},
)
