:py:mod:`pyfeyn2.render.pyx.deco`
=================================

.. py:module:: pyfeyn2.render.pyx.deco

.. autoapi-nested-parse::

   A couple of classes for decorating diagram elements.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.deco.Arrow
   pyfeyn2.render.pyx.deco.FreeArrow
   pyfeyn2.render.pyx.deco.ParallelArrow
   pyfeyn2.render.pyx.deco.Label
   pyfeyn2.render.pyx.deco.PointLabel
   pyfeyn2.render.pyx.deco.LineLabel



Functions
~~~~~~~~~

.. autoapisummary::

   pyfeyn2.render.pyx.deco.getarrowpath



.. py:function:: getarrowpath(arrowtopath, selfpos, var1, selfsize, var2, selfconstriction, constrictionlen)


.. py:class:: Arrow(pos=0.5, size=6 * pyx.unit.v_pt, angle=45, constriction=0.8)

   Bases: :py:obj:`pyx.deco.deco`, :py:obj:`pyx.attr.attr`

   Arrow for Feynman diagram lines

   Constructor.

   .. py:method:: decorate(dp)

      Attach arrow to a path (usually a line).



.. py:class:: FreeArrow(length=0.5 * pyx.unit.v_cm, size=6 * pyx.unit.v_pt, angle=45, constriction=0.8, pos=None, x=None, y=None, direction=0)

   Bases: :py:obj:`pyfeyn2.render.pyx.utils.Visible`

   Arrow not attached to any line in a diagram.

   Constructor.

   .. py:method:: draw(canvas)

      Draw this arrow on the supplied canvas.



.. py:class:: ParallelArrow(line, pos=0.5, displace=0.3, length=0.5 * pyx.unit.v_cm, size=6 * pyx.unit.v_pt, angle=45, constriction=0.8, sense=+1, curved=False, stems=1, stemsep=0.03)

   Bases: :py:obj:`pyfeyn2.render.pyx.utils.Visible`

   Arrow running parallel to a line, for momenta, helicities etc.

   Constructor.

   .. py:method:: draw(canvas)

      Draw this arrow on the supplied canvas.



.. py:class:: Label(text, pos=None, x=None, y=None, size=pyx.text.size.normalsize)

   Bases: :py:obj:`pyfeyn2.render.pyx.utils.Visible`

   General label, unattached to any diagram elements

   Constructor.

   .. py:method:: draw(canvas)

      Draw this label on the supplied canvas.



.. py:class:: PointLabel(point, text, displace=0.3, angle=0, size=pyx.text.size.normalsize)

   Bases: :py:obj:`Label`

   Label attached to points on the diagram

   Constructor.

   .. py:method:: getPoint()

      Get the point associated with this label.


   .. py:method:: setPoint(point)

      Set the point associated with this label.


   .. py:method:: draw(canvas)

      Draw this label on the supplied canvas.



.. py:class:: LineLabel(line, text, pos=0.5, displace=0.3, angle=0, size=pyx.text.size.normalsize)

   Bases: :py:obj:`Label`

   Label for Feynman diagram lines

   Constructor.

   .. py:method:: getLine()

      Get the associated line.


   .. py:method:: setLine(line)

      Set the associated line.


   .. py:method:: draw(canvas)

      Draw this label on the supplied canvas.
