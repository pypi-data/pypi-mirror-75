import re
import pathlib
import os
from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

# parse the version instead of importing it to avoid dependency-related crashes
with open("src/_repobee/__version.py", mode="r", encoding="utf-8") as f:
    line = f.readline()
    __version__ = line.split("=")[1].strip(" '\"\n")
    assert re.match(r"^\d+(\.\d+){2}(-(alpha|beta|rc)(\.\d+)?)?$", __version__)

python_interpreter = os.getenv("REPOBEE_PYTHON_INTERPRETER")
if python_interpreter:  # install with RepoBee's install script
    pathlib.Path("src/_repobee/distinfo.py").write_text(
        f"""
import pathlib
DIST_INSTALL = True
PYTHON_INTERPRETER = pathlib.Path('{python_interpreter}')
"""
    )


test_requirements = [
    "pytest>=4.0.0",
    "pytest-cov>=2.6.1",
    "pytest-mock",
    "codecov",
    "bandit",
    "flake8",
    "black",
]
docs_requirements = [
    "sphinx>=1.8.2",
    "sphinx-autodoc-typehints",
    "sphinx_rtd_theme",
    "sphinx-argparse",
]
required = [
    "appdirs",
    "daiquiri",
    "pygithub",
    "colored",
    "python-gitlab==1.15.0",
    "pluggy>=0.13.1",
]

setup(
    name="repobee",
    version=__version__,
    description=(
        "A CLI tool for managing large amounts of GitHub repositories"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Simon Larsén",
    author_email="slarse@kth.se",
    url="https://github.com/repobee/repobee",
    download_url=(
        "https://github.com/repobee/repobee/archive/v{}.tar.gz".format(
            __version__
        )
    ),
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=("tests", "docs")),
    py_modules=["repobee"],
    tests_require=test_requirements,
    install_requires=required,
    extras_require=dict(TEST=test_requirements, DOCS=docs_requirements),
    entry_points=dict(console_scripts="repobee = repobee:main"),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)
