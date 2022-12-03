:py:mod:`pyfeyn2.render.pyx.config`
===================================

.. py:module:: pyfeyn2.render.pyx.config

.. autoapi-nested-parse::

   Handle runtime options and command line option parsing.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.config.OptionSet



Functions
~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.config.addPyfeynOptions
   pyfeyn2.render.pyx.config.processOptions
   pyfeyn2.render.pyx.config.getOptions



Attributes
~~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.config._opts


.. py:function:: addPyfeynOptions(parser)

   Add the PyFeyn options to the options parser's option set.


.. py:function:: processOptions(parser=None)

   Process the given options.


.. py:class:: OptionSet

   A container for options.


.. py:data:: _opts
   

   

.. py:function:: getOptions()

   Return the (unique) option set.
