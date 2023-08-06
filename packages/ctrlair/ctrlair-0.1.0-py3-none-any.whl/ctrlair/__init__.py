import pathlib

home = pathlib.Path(__file__).parents[2].resolve()
version = (home / "VERSION").read_text()

__version__ = version
__author__ = "João Palmeiro"
