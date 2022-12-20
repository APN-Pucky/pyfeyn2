FeynML
======

FeynML is a project to develop an XML dialect for describing Feynman diagrams as used in quantum field theory calculations. 
The primary aim is to unambiguously describe the structure of a diagram in XML, giving a de facto representation for diagram structure which can be easily translated into another representation. 

Why XML?
~~~~~~~~~~

Okay, XML is a bit of a buzzword. Not everything is best-represented as XML. 
However, it does have several benefits: 

* it is simple to read and write, both for humans and computers; 
* there are a variety of technologies available for parsing, styling and transforming XML (see e.g. SAX, DOM, CSS, XSLT)
* its heirarchical structure maps fairly well into describing graphs. 

The variety of technologies aspect is probably the most important. 


.. _elements:

Elements
~~~~~~~~~~
A Feynman diagram is constructed of these the minimal building blocks of a diagram:

.. toctree::
   :glob:
   :maxdepth: 3

   leg.rst
   vertex.rst
   propagator.rst
   label.rst

.. _attributes:

Attributes
~~~~~~~~~~~
Above buildings blocks come with different attributes, which are described in the following sections

.. include:: ../shared/attr_tab.rst

.. toctree::
   :glob:
   :maxdepth: 3
   :hidden:

   attributes/*

The attributes provide additional information and metadata about the elements.

Examples
~~~~~~~~~~

.. toctree::
   :glob:
   :maxdepth: 3

   FeynML.ipynb
