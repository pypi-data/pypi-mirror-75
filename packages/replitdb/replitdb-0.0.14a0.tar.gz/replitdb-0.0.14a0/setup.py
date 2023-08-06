import setuptools
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="replitdb",
    version="0.0.14a0",
    author="codemonkey51",
    author_email='pypi@codemonkey51.dev',
    description="a client for replit db",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://github.com/Codemonkey51/replit-db-client",
    install_requires=[
      'requests_async'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['repldb=replitdb:command_main'],
    },
    python_requires='>=3.6',
)