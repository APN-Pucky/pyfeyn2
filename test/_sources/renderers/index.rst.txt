Renderers
================================

Most of the renderers are implemented in the :mod:`pyfeyn2.render` module.

The once based on latex are in :mod:`pyfeyn2.render.latex`. 
They offer the function :meth:`pyfeyn2.render.latex.LatexRender.get_src_diag` to get the latex source for rendering this diagram or the whole latex source via :meth:`pyfeyn2.render.latex.LatexRender.get_src`.
Some more specialized renderers offer their source through different functions like :meth:`pyfeyn2.render.dot.DotRender.get_src_dot`.


.. toctree::
    :glob:
    :maxdepth: 2

    **
