=======================================
MadGraph Export Plugin Integration
=======================================

.. code-block:: bash

   pip install --upgrade feynml[interfaces]

.. note::
    
    FeynML Must be above version 0.2.23.

Ensure that you also use the MadGraph export plugin by following these steps:

1. Create a file at `/MG5_aMC_v3_5_1/PLUGIN/MadFeynML/__init__.py`.
2. In the file, include the line: ``from feynml.interface.madgraph.plugin import *``.
3. Execute the following madgraph script:

.. code-block:: bash

   generate p p > t t~
   output feynml OUTDIRNAME --draw

If you omit ``--draw``, it will only provide the `.fml` file, which you can load in Python using https://pyfeyn2.readthedocs.io/en/stable/_autosummary/feynml.feynml.FeynML.html#feynml.feynml.FeynML.from_xml.
