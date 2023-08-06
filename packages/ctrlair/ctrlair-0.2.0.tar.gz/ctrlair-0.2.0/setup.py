import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


def get_version(root: pathlib.Path, rel_path: str) -> str:
    for line in (root / rel_path).read_text().splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="ctrlair",
    version=get_version(here, "src/ctrlair/__init__.py"),
    description="A toolbox for Altair.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joaopalmeiro/ctrlair",
    author="João Palmeiro",
    author_email="jm.palmeiro@campus.fct.unl.pt",
    license="MIT",
    # List of classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="altair, data, visualization",
    package_dir={"": "src"},
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["altair"],
    project_urls={
        "Bug Reports": "https://github.com/joaopalmeiro/ctrlair/issues",
        "Source": "https://github.com/joaopalmeiro/ctrlair",
    },
)
