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

CSS
~~~~~~~
To style the diagram, the following CSS classes are available:

.. code-block:: css

   /* General */
   * { ... }                              /* all elements */
   #`id` { ... }                          /* the element with id */

   /* diagram */
   vertex { ... }                         /* all vertices */
   propagator { ... }                     /* all propagators */
   leg { ... }                            /* all legs */

   /* attributes */
   [type=`type`] { ... }                  /* everything of given type */
   [pdgid="`pdgid`"] { ... }              /* all pdg particles of given id*/

Variables in single quotes are replaced by the actual value.
The available css declarations are listed in the :ref:`style`.
For a list of types see :ref:`type`.

With the :ref:`class` attribute, the user can add custom classes to the elements.
These or above classes can also be applied to a subset of the diagram e.g. 

.. code-block:: css

   propagator:not([pdgid="-24"]) { ... }  /* all propagators except W- bosons */

The groupings of CSS are often more practical than looping through the elements in the diagram adjusting their style.
For more advanced CSS selectors see https://www.w3schools.com/cssref/css_selectors.php.


Examples
~~~~~~~~~~

.. toctree::
   :glob:
   :maxdepth: 3

   FeynML.ipynb

More examples can be found in the :ref:`gallery` and the different renderers are listed in :ref:`renderers`.
