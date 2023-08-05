
JGF(Z) format implementation
============================

This package implements export and import functions for the JSON Graph Format (gZipped) ``JGF(Z)`` (https://jsongraphformat.info). Supported input formats/libraries are ``networkx``\ , ``igraph``\ , ``numpy`` matrices and ``JXNF`` files. All network, node and edges attributes are saved as well.

This project is being developed to support the new network datatype for (brainlife.io).

Authors
^^^^^^^


* `Filipi N. Silva <filsilva@iu.edu>`_


.. raw:: html

   <!-- ### Contributors
   - Franco Pestilli (franpest@indiana.edu) -->



Funding
^^^^^^^


.. image:: https://img.shields.io/badge/NIH-1R01EB029272_01-blue.svg
   :target: https://www.nibib.nih.gov/node/113361
   :alt: NIH-1R01EB029272-01



.. raw:: html

   <!-- ### Citations

   1. Adai, Alex T., Shailesh V. Date, Shannon Wieland, and Edward M. Marcotte. "LGL: creating a map of protein function with an algorithm for visualizing very large biological networks." Journal of molecular biology 340, no. 1 (2004): 179-190. [https://doi.org/10.1016/j.jmb.2004.04.047](https://doi.org/10.1016/j.jmb.2004.04.047) -->



Installation
------------

You can install this package using ``pip``\ :

.. code-block:: bash

   pip install jgf

or install it from this git repository:

.. code-block:: bash

   git clone <repository URL>
   cd <repository PATH>
   pip install -e ./

API Reference
-------------

API reference can be found in (https://jgf.readthedocs.io/).

Example of use
--------------

To use the library in igraph environment simply import the correct module and run ``save`` or ``load`` functions:

.. code-block:: python

   import igraph as ig
   import jgf.igraph as jig

   g = ig.Graph.Famous("Zachary")

   # will save a compressed file
   jig.save(g,"zachary.jgfz")

   g, = jig.load("zachary.jgfz")

You can also use it to save and load connectivity matrices as square numpy matrices:

.. code-block:: python

   import numpy as np
   import jgf.conmat as jcm

   A = np.array([
     [  0, 0.1, 0.2,   0,   0],
     [  0,   0,   0, 0.5,   0],
     [  0,   0,   0,   0, 1.0],
     [1.0, 1.0,   0,   0,   0],
     [  0,   0, 0.5,   0,   0],
     ])

   nodeProperties = {
     "name" : [
       "Node 1",
       "Node 2",
       "Node 3",
       "Node 4",
       "Node 5",
     ]
   }
   # will save a compressed file
   jcm.save(A,"example.jgfz",label= "Example", nodeProperties=nodeProperties)

   B,properties = jcm.load("example.jgfz",getExtraData=True)
