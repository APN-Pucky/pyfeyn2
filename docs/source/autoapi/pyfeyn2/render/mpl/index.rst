:py:mod:`pyfeyn2.render.mpl`
============================

.. py:module:: pyfeyn2.render.mpl


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.mpl.MPLRender



Functions
~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.mpl.line
   pyfeyn2.render.mpl.spring



.. py:function:: line(p1, p2, points=200)


.. py:function:: spring(xp1, xp2, points=200, rot=3, amp=0.15, line_frac=0.2)


.. py:class:: MPLRender(fd, *args, **kwargs)

   Bases: :py:obj:`pyfeyn2.render.render.Render`

   .. py:method:: render(file=None, show=True, width=None, height=None, resolution=100)
