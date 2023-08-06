import setuptools
from version import get_version


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ['sqlalchemy', 'pymysql']

setuptools.setup(
    name="dblit",
    version=get_version(),
    author="Matthias Burbach",
    author_email="matthias.burbach@web.de",
    description="A library for persistent management of machine learning ground truth labeling jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BigNerd/dblit",
    packages=setuptools.find_packages(include=("dblit", "dblit.*")),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
