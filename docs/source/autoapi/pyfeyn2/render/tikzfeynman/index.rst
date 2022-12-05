:py:mod:`pyfeyn2.render.tikzfeynman`
====================================

.. py:module:: pyfeyn2.render.tikzfeynman


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.tikzfeynman.TikzFeynmanRender



Functions
~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.tikzfeynman.feynman_to_tikz_feynman



Attributes
~~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.tikzfeynman.type_map


.. py:data:: type_map
   

   

.. py:function:: feynman_to_tikz_feynman(fd)


.. py:class:: TikzFeynmanRender(fd, documentclass='standalone', document_options=['preview', 'crop', 'tikz'], *args, **kwargs)

   Bases: :py:obj:`pyfeyn2.render.latex.LatexRender`

   A class that contains a full LaTeX document.

   If needed, you can append stuff to the preamble or the packages.
   For instance, if you need to use ``\maketitle`` you can add the title,
   author and date commands to the preamble to make it work.


   :param default_filepath: The default path to save files.
   :type default_filepath: str
   :param documentclass: The LaTeX class of the document.
   :type documentclass: str or `~.Command`
   :param document_options: The options to supply to the documentclass
   :type document_options: str or `list`
   :param fontenc: The option for the fontenc package. If it is `None`, the fontenc
                   package will not be loaded at all.
   :type fontenc: str
   :param inputenc: The option for the inputenc package. If it is `None`, the inputenc
                    package will not be loaded at all.
   :type inputenc: str
   :param font_size: The font size to declare as normalsize
   :type font_size: str
   :param lmodern: Use the Latin Modern font. This is a font that contains more glyphs
                   than the standard LaTeX font.
   :type lmodern: bool
   :param textcomp: Adds even more glyphs, for instance the Euro (€) sign.
   :type textcomp: bool
   :param page_numbers: Adds the ability to add the last page to the document.
   :type page_numbers: bool
   :param indent: Determines whether or not the document requires indentation. If it
                  is `None` it will use the value from the active config. Which is
                  `True` by default.
   :type indent: bool
   :param geometry_options: The options to supply to the geometry package
   :type geometry_options: dict
   :param data: Initial content of the document.
   :type data: list

   .. py:method:: valid_type()
