:py:mod:`pyfeyn2.render.pyx.lines`
==================================

.. py:module:: pyfeyn2.render.pyx.lines

.. autoapi-nested-parse::

   Various particle line types.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.lines.Line
   pyfeyn2.render.pyx.lines.MultiLine
   pyfeyn2.render.pyx.lines.Scalar
   pyfeyn2.render.pyx.lines.Ghost
   pyfeyn2.render.pyx.lines.DecoratedLine
   pyfeyn2.render.pyx.lines.Gluon
   pyfeyn2.render.pyx.lines.Vector
   pyfeyn2.render.pyx.lines.Graviton
   pyfeyn2.render.pyx.lines.Gaugino
   pyfeyn2.render.pyx.lines.Gluino
   pyfeyn2.render.pyx.lines.Gravitino
   pyfeyn2.render.pyx.lines.Phantom




Attributes
~~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.lines.Fermion
   pyfeyn2.render.pyx.lines.Higgs
   pyfeyn2.render.pyx.lines.Sfermion
   pyfeyn2.render.pyx.lines.Photon
   pyfeyn2.render.pyx.lines.NamedLine


.. py:class:: Line(point1, point2)

   Bases: :py:obj:`pyfeyn2.render.pyx.utils.Visible`

   Base class for all objects which connect points in Feynman diagrams

   Constructor.

   .. py:method:: addLabel(text, pos=0.5, displace=-0.25, angle=0, size=pyx.text.size.normalsize)

      Add a LaTeX label to this line, either via parameters or actually as
      a TeXLabel object.


   .. py:method:: addParallelArrow(pos=0.5, displace=0.3, length=0.5 * pyx.unit.v_cm, size=6 * pyx.unit.v_pt, angle=45, constriction=0.8, sense=+1, curved=False, stems=1, stemsep=0.03)

      Add an arrow pointing along the line.


   .. py:method:: removeLabels()

      Remove the labels from this line.


   .. py:method:: fracpoint(frac)

      Get a new Point representing the point at the given fraction along
      the fundamental line (i.e. no truncation or deformation).
      TODO: Handle units properly.


   .. py:method:: setArrows(arrows)

      Define the arrows on this line.


   .. py:method:: addArrow(position=0.53, arrow=None)

      Add an arrow to the line at the specified position, which is a number
      between 0 and 1, representing the fraction along the line at which the
      arrow should be placed. The default arrow style can be overridden by
      explicitly supplying an arrow object as the 'arrow' argument, in which
      case the position argument will be ignored.


   .. py:method:: removeArrows()

      Remove all arrows from this line.


   .. py:method:: arcThru(arcpoint=None, x=None, y=None)

      Set the point through which this line will arc. Either pass a Point
      or set x, y as floats.


   .. py:method:: straighten()

      Make this line a straight line between start and end.


   .. py:method:: bend(amount)

      Bend the line to the right by a given distance.


   .. py:method:: set3D(choice)

      Make this line display in '3D'.


   .. py:method:: getStyles(stylelist)

      Get the styles associated with this line.


   .. py:method:: setStyles(stylelist)

      Set the styles associated with this line.


   .. py:method:: addStyle(style)

      Add a style to this line.


   .. py:method:: addStyles(stylelist)

      Add some styles to this line.


   .. py:method:: getPath()

      Get the path taken by this line.


   .. py:method:: getVisiblePath()

      Find the subpath between the endpoints which isn't overshadowed by a blob of some kind


   .. py:method:: draw(canvas)

      Drwa this line on the given canvas.



.. py:data:: Fermion
   

   

.. py:class:: MultiLine(point1, point2, n=5, dist=0.2)

   Bases: :py:obj:`Line`

   A class for drawing multiple parallel straight lines.

   Constructor.

   .. py:method:: draw(canvas)

      Draw this multiline on the supplied canvas.



.. py:class:: Scalar(point1, point2)

   Bases: :py:obj:`Line`

   A scalar particle line, like a Higgs boson.

   Constructor.

   .. py:method:: draw(canvas)

      Draw this scalar line on the given canvas.



.. py:data:: Higgs
   

   

.. py:data:: Sfermion
   

   

.. py:class:: Ghost(point1, point2)

   Bases: :py:obj:`Line`

   A dotted scalar particle line, like a Yang-Mills ghost particle.

   Constructor.

   .. py:method:: draw(canvas)

      Draw this scalar line on the given canvas.



.. py:class:: DecoratedLine(point1, point2)

   Bases: :py:obj:`Line`

   Base class for spring and sine-like lines

   Constructor.

   .. py:method:: invert()

      Reflect the line decoration about the line.


   .. py:method:: getNumHalfCycles()

      Get the number of half cycles in this line.


   .. py:method:: getDeformedPath()

      Get the deformed path.



.. py:class:: Gluon(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   A line with a cycloid deformation

   Constructor.

   .. py:method:: set3D(is3D=True, skipsize=pyx.unit.length(0.04), parity=0)

      Make this line display in '3D'.


   .. py:method:: invert()

      Flip the line decoration around the line.


   .. py:method:: getFrequency()

      Get the rate of occurence of the coil decoration.


   .. py:method:: setFrequency(freq)

      Set the rate of occurence of the coil decoration.


   .. py:method:: getAmplitude()

      Get the radius of the coil decoration.


   .. py:method:: setAmplitude(amplitude)

      Set the radius of the coil decoration.


   .. py:method:: setExtraCycles(extras)

      Add some extra (possibly negative) oscillations to the coil decoration.


   .. py:method:: getDeformedPath()

      Get the path modified by the coil warping.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:class:: Vector(point1, point2, amplitude=0.25, frequency=1.0)

   Bases: :py:obj:`DecoratedLine`

   A line with a sinoid deformation

   Constructor.

   .. py:method:: invert()

      Reflect the decoration in the line itself.


   .. py:method:: getFrequency()

      Get the rate of occurance of the oscillation.


   .. py:method:: setFrequency(freq)

      Set the rate of occurance of the oscillation.


   .. py:method:: getAmplitude()

      Get the size of the oscillation.


   .. py:method:: setAmplitude(amplitude)

      Set the size of the oscillation.


   .. py:method:: setExtraHalfCycles(extras)

      Add some extra half cycles to the oscillation on top of those
      determined from the frequency.


   .. py:method:: getDeformedPath()

      Get the path with the decorative deformation.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:data:: Photon
   

   

.. py:class:: Graviton(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   A line with a double sinoid deformation

   Constructor.

   .. py:method:: set3D(is3D=True, skipsize=pyx.unit.length(0.04), parity=0)

      Make this line display in '3D'.


   .. py:method:: invert()

      Reflect the decoration in the line itself.


   .. py:method:: getDeformedPath(sign=1)

      Get the path with the decorative deformation.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:class:: Gaugino(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   A line with a sinoid deformation and a normal line

   Constructor.

   .. py:method:: set3D(is3D=True, skipsize=pyx.unit.length(0.04), parity=0)

      Make the line look 3-dimensional by 'cutting' one line where self-intersections occur.


   .. py:method:: invert()

      Reflect the decoration in the line itself.


   .. py:method:: getDeformedPath()

      Get the path with the decorative deformation.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:class:: Gluino(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   A line with a cycloid deformation and a normal line

   Constructor.

   .. py:method:: set3D(is3D=True, skipsize=pyx.unit.length(0.04), parity=0)

      Make this line display in '3D'.


   .. py:method:: invert()

      Reflect the decoration in the line itself.


   .. py:method:: getDeformedPath()

      Get the path with the decorative deformation.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:class:: Gravitino(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   A line with a double sinoid deformation and a simple line

   Constructor.

   .. py:method:: set3D(is3D=True, skipsize=pyx.unit.length(0.04), parity=0)

      Make this line display in '3D'.


   .. py:method:: invert()

      Reflect the decoration in the line itself.


   .. py:method:: getDeformedPath(sign=1)

      Get the path with the decorative deformation.


   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas.



.. py:class:: Phantom(point1, point2)

   Bases: :py:obj:`DecoratedLine`

   An invisible line.

   Constructor.

   .. py:method:: draw(canvas)

      Draw the line on the supplied canvas (does nothing for a phantom).



.. py:data:: NamedLine
   

   
