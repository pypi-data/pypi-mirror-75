import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subcaretin",
    version="0.1.0",
    scripts=['bin/subcaretin'],
    author="Vitiko",
    author_email="vhnz98@gmail.com",
    description="Descarga automática de subtítulos desde Argenteam y Subdivx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vitiko123/subcaretin",
    install_requires=[
        "requests",
        "guessit",
        "beautifulsoup4",
        "python-magic",
        "unrar"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
