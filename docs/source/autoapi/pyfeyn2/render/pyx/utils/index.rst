:py:mod:`pyfeyn2.render.pyx.utils`
==================================

.. py:module:: pyfeyn2.render.pyx.utils

.. autoapi-nested-parse::

   Utility functions and classes for PyFeyn



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.utils.Visible



Functions
~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.utils.sign



Attributes
~~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.utils.defunit
   pyfeyn2.render.pyx.utils.todefunit


.. py:data:: defunit
   

   

.. py:data:: todefunit
   

   

.. py:function:: sign(x)

   Get the sign of a numeric type


.. py:class:: Visible

   .. py:method:: isVisible()

      Check if this instance is visible.


   .. py:method:: getPath()

      Return the path of this instance.


   .. py:method:: getVisiblePath()

      Return the visible path of this instance.


   .. py:method:: setDepth(depth)

      Set the depth at which this instance lives.


   .. py:method:: getDepth()

      Return the depth at which this instance lives.


   .. py:method:: __cmp__(other)

      Compare with another visible class, just using layers.
