# PyFeyn2

Forked from <https://pyfeyn.hepforge.org/> 

PyFeyn is a Python-language based system for drawing Feynman diagrams. It was inspired by the C++ FeynDiagram system, and aims to provide the same functionality and quality of output as that, with the added benefits of a modern interpreted language, an improved interface and output direct to both EPS and PDF. Behind the scenes, PyFeyn uses the excellent PyX system - you can use PyX constructs in PyFeyn diagrams if you want, too.

[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/pyfeyn2.svg) [![DOI](https://zenodo.org/badge/571974255.svg)](https://zenodo.org/badge/latestdoi/571974255)

[![test][a t image]][a t link]      [![Coverage Status][c t i]][c t l]  [![Codacy Badge][cc c i]][cc c l]   [![Codacy Badge][cc q i]][cc q l]  [![Documentation][rtd t i]][rtd t l] [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/APN-Pucky/pyhep-2023/final)

## Dependencies

*   libmagickwand-dev (to display pdfs in a jupyter-notebook, might require a policy change of the imagemagick config for PDFs, see Troubleshooting)
*   ghostscript
*   latexmk
*   (graphviz)
*   (feynmp-auto/feynmf)

## Installation

```sh
poerty install --with docs --with dev
poetry shell
```

## Documentation

*   <https://pyfeyn2.readthedocs.io/en/stable/>
*   <https://apn-pucky.github.io/pyfeyn2/index.html>

## Similar Feynman diagram rendering project:

*   <https://github.com/ndeutschmann/qgraf-xml-drawer>
*   <https://github.com/GkAntonius/feynman>
*   <https://github.com/JP-Ellis/tikz-feynman>
*   <https://pyfeyn.hepforge.org/> 
*   <https://feynml.hepforge.org/>
*   <http://www.feyndiagram.com/>

Several of these are integrated into pyfeyn2.

## Troubleshooting

*   [ImageMagick security policy 'PDF' blocking conversion]( https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion )
*   [Graphviz missing on mac](https://graphviz.org/download/#mac)

## Development


### package/python structure:

*   <https://mathspp.com/blog/how-to-create-a-python-package-in-2022>
*   <https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/>

[pypi image]: https://badge.fury.io/py/pyfeyn2.svg
[pypi link]: https://pypi.org/project/pyfeyn2/
[pypi versions]: https://img.shields.io/pypi/pyversions/pyfeyn2.svg

[a t link]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml
[a t image]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml/badge.svg

[cc q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44
[cc q l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/pyfeyn2&amp;utm_campaign=Badge_Grade
[cc c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44
[cc c l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/pyfeyn2&utm_campaign=Badge_Coverage

[c t l]: https://coveralls.io/github/APN-Pucky/pyfeyn2?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/pyfeyn2/badge.svg?branch=master

[rtd t i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=latest
[rtd t l]: https://pyfeyn2.readthedocs.io/en/latest/?badge=latest
