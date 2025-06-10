# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.abspath("../.."))
import copy

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python <= 3.10

from smpl import doc, io

import pyfeyn2
from pyfeyn2.render import all

# -- Project information -----------------------------------------------------


try:
    with open("../../pyproject.toml", "rb") as f:
        info = tomllib.load(f)
except FileNotFoundError:
    with open("pyproject.toml", "rb") as f:
        info = tomllib.load(f)

project = info["project"]["name"]
copyright = str(datetime.datetime.now().year) + ", Alexander Puck Neuwirth"
author = ", ".join([a["name"] for a in info["project"]["authors"]])
version = re.sub("^", "", os.popen("git describe --tags").read().strip())
rst_epilog = f""".. |project| replace:: {project}\n\n"""


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "nbsphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.napoleon",
    "sphinx_math_dollar",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "jupyter_sphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

# nbsphinx_execute = "always"
# nbsphinx_execute = "never"

napoleon_use_ivar = True
# autoapi_type = "python"
# autoapi_dirs = ["../../" + project]
# autoapi_python_class_content = "both"

autosummary_generate = True
# autosummary_imported_members = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
highlight_language = "none"


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_logo = "pyfeyn-logo.svg"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# UTF-8 characters in PDF
latex_engine = "xelatex"

renders = all.renders
styles = all.AllRender.valid_styles()
types = all.AllRender.valid_types()
shapes = all.AllRender.valid_shapes()
attributes = all.AllRender.valid_attributes()

rst_epilog = (
    rst_epilog
    + """
.. |check| replace:: ✔


.. |uncheck| replace:: ✖


.. |mixed| replace:: ✔/✖

"""
)
for n, r in renders.items():
    for s in styles:
        rst_epilog += (
            f".. |{n}.style.{s}| replace:: "
            + ("|check|" if r.valid_style(s) else "|uncheck|")
            + "\n\n"
        )
    for s in types:
        rst_epilog += (
            f".. |{n}.type.{s}| replace:: "
            + ("|check|" if r.valid_type(s) else "|uncheck|")
            + "\n\n"
        )
    for s in shapes:
        rst_epilog += (
            f".. |{n}.shape.{s}| replace:: "
            + ("|check|" if r.valid_shape(s) else "|uncheck|")
            + "\n\n"
        )
    for s in attributes:
        rst_epilog += (
            f".. |{n}.attribute.{s}| replace:: "
            + ("|check|" if r.valid_attribute(s) else "|uncheck|")
            + "\n\n"
        )


style_tab = {":ref:`style`": [v for v in renders.keys()]}
original = copy.copy(style_tab)
for s in styles:
    arr = []
    for n, r in renders.items():
        arr += [f"|{n}.style.{s}|"]
    style_tab[f":ref:`{s}`"] = arr
    io.write(
        "shared/style/" + s + ".rst",
        doc.array_table({**original, f":ref:`{s}`": arr}, tabs=0, init=True),
    )

type_tab = {":ref:`type`": [v for v in renders.keys()]}
original = copy.copy(type_tab)
for s in types:
    arr = []
    for n, r in renders.items():
        arr += [f"|{n}.type.{s}|"]
    type_tab[f":ref:`/feynml/attributes/type/{s}.ipynb`"] = arr

shape_tab = {":ref:`type`": [v for v in renders.keys()]}
original = copy.copy(shape_tab)
for s in shapes:
    arr = []
    for n, r in renders.items():
        arr += [f"|{n}.shape.{s}|"]
    shape_tab[f":ref:`/feynml/attributes/shape/{s}.ipynb`"] = arr

attr_tab = {":ref:`attributes`": [v for v in renders.keys()]}
original = copy.copy(attr_tab)
for s in attributes:
    arr = []
    for n, r in renders.items():
        arr += [f"|{n}.attribute.{s}|"]
    attr_tab[f":ref:`{s}`"] = arr
    io.write(
        "shared/attribute/" + s + ".rst",
        doc.array_table({**original, f":ref:`{s}`": arr}, tabs=0, init=True),
    )


io.write("shared/style_tab.rst", doc.array_table(style_tab, tabs=0, init=True))
io.write("shared/type_tab.rst", doc.array_table(type_tab, tabs=0, init=True))
io.write("shared/shape_tab.rst", doc.array_table(shape_tab, tabs=0, init=True))
io.write("shared/attr_tab.rst", doc.array_table(attr_tab, tabs=0, init=True))
