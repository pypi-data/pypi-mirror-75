import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cmdnote',
    version='0.1.0',
    author='Zian Ke',
    author_email='zian.ke@zian.ke',
    description='Command line tool which stores your future commands',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zianke/cmdnote',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['colorama'],
    entry_points={'console_scripts': ['cmdnote=cmdnote.main:main']}
)
