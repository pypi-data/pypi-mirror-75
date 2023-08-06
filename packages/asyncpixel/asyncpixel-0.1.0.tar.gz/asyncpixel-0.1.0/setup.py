import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncpixel",
    version="0.1.0",
    author="Leon Bowie",
    author_email="leon@bowie-co.nz",
    description="An async wrapper for hypixel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obsidion-dev/asyncpixel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiohttp",
    ],
)
