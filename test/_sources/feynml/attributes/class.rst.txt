.. _class:

class
=====
| Format: String
| Elements: :ref:`leg`, :ref:`propagator`, :ref:`vertex`
| Implementation: :py:class:`pyfeyn2.feynmandiagram.Styled`

The class element is used to define a class of particles. 
They can be used to define a set of particles with the same style.

Special classes are inferred from :ref:`pdgid` to ``"pdgid" + pdgid`` the and from :ref:`type`.

.. include:: ../../shared/attribute/class.rst
