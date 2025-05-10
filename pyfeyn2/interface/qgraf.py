"""Moved to :py:mod:`feynml.interface.qgraf`"""
from feynml.interface.qgraf import get_style as _get_style
from smpl_doc.doc import deprecated

get_style = deprecated("2.2.6", "Directly use feynml.interface.qgraf.get_style()")(
    _get_style
)
