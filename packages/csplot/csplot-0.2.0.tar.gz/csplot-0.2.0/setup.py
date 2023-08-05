import setuptools

with open('README.md', 'r') as f_readme:
    description = f_readme.read()

setuptools.setup(
    name="csplot",
    version="0.2.0",
    author="Grzesiek11",
    author_email="grzesiek.jedenastka@outlook.com",
    description="Simple library for plotting charts from Code::Stats API",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/grzesiek11/csplot",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)