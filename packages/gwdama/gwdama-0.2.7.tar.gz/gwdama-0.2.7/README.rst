GWdama
======

This package aims at providing a unified and easy to use interface to access and manipulate Gravitational Wave data. This can be read from different sources, as in local `fram files (gwf) <https://lappweb.in2p3.fr/virgo/FrameL/>`_ and especially from the `Gravitational Wave Open Science Center <https://www.gw-openscience.org/>`_. It will also include some convenient plotting and data analysis methods aimed at Detector Characterization.

----------------
Package overview
----------------

The package currently comprises a main class, ``GwDataManager``, which acts as a container for data (not only related to GW's). This is based on `h5py.File class <http://docs.h5py.org/en/stable/high/file.html>`_ with the addition of the methods and the attributes to import and manipulate GW data. Differently from the common application of ``h5py.File`` objects, a ``GwDataManager`` instance can be set to occupy only a temporary file, which is authomatically deleted by python once closed, or some space in the RAM. Refer to the `full documentation <'https://gwdama.readthedocs.io/en/latest/index.html'>`_ for further details. 

The basic data format to contain the data is a `h5py.Dataset like <http://docs.h5py.org/en/stable/high/dataset.html>`_ object. These Dataset are created within an instance of ``GwDataManager()`` with the usual methods of ``h5py``: ``create_dataset(name, shape, dtype)``. They contain data, typically of numeric type but also strings in case, and some convenient attributes. For example, for GW data, and in general all time series, it is important the information of when they have been recorded, and at which sampling frequency. This can be conveniently added and customised. Also a ``GwDatamanager`` object contains attributes for itself.

When the data have been acquired and possibly pre-processed, they can be saved to ``hdf5`` format, and later read back.

-----------------
Quick start guide
-----------------

GWdama can be installed via `pip <https://docs.python.org/3/installing/index.html>`_,

.. code-block:: console

    $ pip install gwdama

and requires Python 3.6.0 or higher.

.. note:: It is usually highly recommended to perform the previous installation within a `python virtual environment <https://docs.python.org/3.6/tutorial/venv.html>`_. The guide to do so can be found in the `full documentation <'https://gwdama.readthedocs.io/en/latest/index.html'>`_.

It can be used programmatically from terminal or within a python script:
::

    >>> from gwdama.io import GwDataManager
    
Creating a dataset
------------------

A dataset of, say, random numbers can be created as:
::

    >>> from gwdama.io import GwDataManager
    >>> import numpy as np
    
    >>> dama = GwDataManager("my_dama")
    >>> dama.create_dataset('random_n', data=np.random.normal(0, 1, (10,)))
    >>> dama.create_dataset('a_list', data=[1, 2, 3, 4])
    >>> dama.create_dataset('a_string', data="this is a string")
    
Then, we can show the contet of this object by:
::

    >>> print(dama)
    my_dama:
      ├── a_list
      ├── a_string
      └── random_n

      Attributes:
         dama_name : my_dama
        time_stamp : 20-07-28_19h36m47s
    
Other attributes can be added to both the ``GwDataManager`` and the Datasets therein:


Reading open data
-----------------

::

    >>> from gwpy.time import to_gps
    
    >>> e_gps = to_gps("2017-08-14 12:00")

    >>> dama = GwDataManager()  # Default name 'mydama' assigned to the dictionary

    >>> dama.read_gwdata(e_gps - 50, e_gps +50, ifo='L1',                # Required params
                         m_data_source="gwosc-remote", dts_key='online', # Optional but useful for giving names to things
                         nproc=6, cache=True, verbose=True)              # Optional to improve performance etc.