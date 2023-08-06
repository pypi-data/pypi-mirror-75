=========
pycellfit
=========

.. image:: https://travis-ci.com/NilaiVemula/pycellfit.svg?branch=master
  :target: https://travis-ci.com/NilaiVemula/pycellfit
.. image:: https://codecov.io/gh/NilaiVemula/pycellfit/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/NilaiVemula/pycellfit
.. image:: https://readthedocs.org/projects/pycellfit/badge/?version=latest
  :target: https://pycellfit.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://badge.fury.io/py/pycellfit.svg
  :target: https://badge.fury.io/py/pycellfit

Project Description
-------------------
**pycellfit**: an open-source Python implementation of the CellFIT method of inferring cellular forces developed by Brodland et al.

**Author**: Nilai Vemula, Vanderbilt University (working under Dr. Shane Hutson, Vanderbilt University)

**Project Goal**: To develop an open-source version of CellFIT, a toolkit for inferring tensions along cell membranes and pressures inside cells based on cell geometries and their curvilinear boundaries. (See [1]_.)

**Project Timeline**: Initial project started in August 2019 with work based off of XJ Xu. This repository was re-made in May 2020 in order to restart repository structure.

**Project Status**: **Development**

Getting Started
---------------
This project is available on `PyPI <https://pypi.org/project/pycellfit/>`_ and can be installed using pip.

It recommended that users make a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ and then install
the package as such:

Install from PyPI:
^^^^^^^^^^^^^^^^^^
.. code:: bash

   pip install pycellfit

Or compile from source:
^^^^^^^^^^^^^^^^^^^^^^^
.. code:: bash

   git clone https://github.com/NilaiVemula/pycellfit.git
   cd pycellfit
   python setup.py install

Full documentation for this package can be found on `readthedocs <https://pycellfit.readthedocs.io/>`_.

Dependencies
^^^^^^^^^^^^
This project is written in Python and has been tested on Python 3.7 and 3.8 on Linux and Windows. This project
primarily
depends
on numpy,
scipy, matplotlib, and other common python packages common in scientific computing. Additionally, `Pillow
<https://github.com/python-pillow/Pillow>`_ is required for reading in input image files. A full list of dependencies
is available in the requirements.txt_ file. All dependencies should be automatically installed when running pip install.

.. _requirements.txt: requirements.txt

Development
-----------
This project is under active development and not ready for public use. The project is built using Travis CI, and all
tests are run with every commit or merge.

Features
--------
Currently, pycellfit supports the following features in the cellular force inference pipeline:

- [ ] converting raw images into segmented images

  - see `SeedWaterSegmenter <https://github
    .com/davidmashburn/SeedWaterSegmenter>`_ or `neural_net_cell_segmenter <https://github
    .com/NilaiVemula/neural_net_cell_segmenter>`_ (work in progress).

- [x] read in segmented images

- [x] convert between watershed and skeleton segmented images

- [x] identify triple junctions

- [ ] identify quad junctions

- [x] generate a mesh

- [x] fit cell edges to circular arcs

- [ ] calculate tangent vectors using circle fits, nearest segment, and chord methods

  - circle fit is incorrect, others have not been added

- [x] calculate tensions

- [ ] calculate pressures

- [x] visualize all of the above steps

Examples
--------
A example walk-through of how to use this module is found in quickstart_.

.. _quickstart: tutorials/README.rst

Future Goals
------------
The final implementation of pycellfit will be as a web-app based on the Django framework. (See `pycellfit-web <https://github.com/NilaiVemula/pycellfit-web>`_)

References
----------
.. [1] Brodland GW, Veldhuis JH, Kim S, Perrone M, Mashburn D, et al. (2014) CellFIT: A Cellular Force-Inference Toolkit Using Curvilinear Cell Boundaries. PLOS ONE 9(6): e99116. https://doi.org/10.1371/journal.pone.0099116

