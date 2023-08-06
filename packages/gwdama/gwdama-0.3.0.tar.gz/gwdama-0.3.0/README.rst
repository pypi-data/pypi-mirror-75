This package aims at providing a unified and easy to use interface to access and manipulate Gravitational Wave data. This can be read from different sources, as in local `frame files (gwf) <https://lappweb.in2p3.fr/virgo/FrameL/>`_ and especially from the `Gravitational Wave Open Science Center <https://www.gw-openscience.org/>`_ (GWOSC). It will also include some convenient plotting and data analysis methods aimed at Detector Characterization.

.. image:: https://readthedocs.org/projects/gwdama/badge/?version=latest
    :target: https://gwdama.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. image:: https://badge.fury.io/py/gwdama.svg
    :target: https://badge.fury.io/py/gwdama

=================================
 GWdata manager package overview
=================================

The package currently comprises a main class, ``GwDataManager``, which behaves as a container for data (not only related to GW's). This is based on `h5py.File class <http://docs.h5py.org/en/stable/high/file.html>`_ with the addition of the methods and the attributes to import and manipulate GW data, and  some functions for data analysis of time series. Differently from the common application of ``h5py.File`` objects, a ``GwDataManager`` instance is, by default, set to occupy only a temporary file, which is authomatically deleted by python once closed, or some space in the RAM. Refer to the `full documentation <'https://gwdama.readthedocs.io/en/latest/index.html'>`_ for further details. 

The basic data format to contain the data is a `h5py.Dataset like <http://docs.h5py.org/en/stable/high/dataset.html>`_ object. These Dataset are created within an instance of ``GwDataManager()`` with the usual methods of ``h5py``: ``create_dataset(name, shape, dtype)``. They contain data, typically of numeric type but also strings in case, and some attributes (or metadata). For example, for GW data, and in general all time series, it is important the information of when they have been recorded, and at which sampling frequency. A neme and a unit are also usefull. This can be conveniently added and customised. Also a ``GwDatamanager`` object contains attributes for itself. Datasets can be also collected into `Groups <http://docs.h5py.org/en/stable/high/group.html>`_.

When the data have been acquired and possibly pre-processed, they can be saved to ``hdf5`` format, and later read back.

===================
 Quick start guide
===================

GWdama can be easily installed via `pip <https://docs.python.org/3/installing/index.html>`_:

.. code-block:: console

    $ pip install gwdama

and requires Python 3.6.0 or higher. The previous command authomatically fulfill all the required dependencies (like on ``numpy`` or ``matplotlib``), so you are ready to start generating datasets and making plots.

It can be used programmatically from terminal or within a python script:
::

    >>> from gwdama.io import GwDataManager
    

.. note::  
    It is usually recommended to perform the previous installation within a `python virtual environment <https://docs.python.org/3.6/tutorial/venv.html>`_.
    Assuming you want to name the environment ``myenv``, 

    .. code-block:: console

        $ python -m venv myenv
        $ source myenv/bin/activate
    
    and the indication ``(myenv)`` will appear on the left of your terminal. It is good practice now to update pip before proceeding to install ``gwdama``:

    .. code-block:: console
    
        (myenv) $ pip install --upgrade pip

    Then, type the command at the beginning of this section and you are ready to go!

    Further details can be found in the `full documentation <'https://gwdama.readthedocs.io/en/latest/index.html'>`_.


--------------------
 Creating a dataset
--------------------

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
::

    >>> dama.attrs['owner'] = 'Francesco'
    >>> dama.show_attrs
    my_dama:
      ├── a_list
      ├── a_string
      └── random_n

      Attributes:
         dama_name : my_dama
             owner : Francesco
        time_stamp : 20-07-28_19h36m47s  
        
Same thing is true for datasets. These can be accessed from their keys, with the same syntax of a dictionsry:
::

    >>> dset = dama['random_n']
    >>> dset.attrs['t0'] = 0         # It is conveninet to use gps times
    >>> dset.attrs['fsample'] = 10   # measured in Hz
    
    >>> dset.show_attrs
    fsample : 10
         t0 : 0

To get back the data contained in this dataset, call its attribute ``data``:
::

    >>> dset.data
    array([-0.73796689, -1.34206706, -0.97898291, -0.19846702,
           -0.85056961,  0.20206334,  0.84720009,  0.19527366,
           -0.9246727 , -0.04808732])

.. note:: Output of random number generator may vary depending on the `random seed <https://numpy.org/doc/stable/reference/random/generated/numpy.random.seed.html?highlight=seed#numpy.random.seed>`_. It is always a good idea to set it before generating anything random with ``np.random.seed(1234)``.

------------------------------
 Writing and reading datasets
------------------------------

Now it is time to **write your data** to disc:
::

    >>> out_f = 'out_dataset.h5'
    >>> write_gwdama_dataset(out_f)
    
Then remember to **close your previous file** before leaving the session:
::

    >>> dama.close()
    >>> del dama       # Redundant but usefull

.. note:: The previous operation is automatically performed every time the session is closed. However, it is good practice to do this manually every time there is no more need of a certain variable.

To **read data** back:
::

    >>> new_dama = GwDataManager(out_f)
    Reading dama
    >>> print(new_dama)
    my_dama:
      ├── a_list
      ├── a_string
      └── random_n

      Attributes:
         dama_name : my_dama
             owner : Francesco
        time_stamp : 20-07-30_12h19m32s



----------------
 Read open data 
----------------

Open data can be accessed from both online and local virtual disks

From online GWOSC
-----------------

::

    >>> from gwpy.time import to_gps                               # Usefull to convert dates to gps times
    
    >>> e_gps = to_gps("2017-08-14 12:00")

    >>> dama = GwDataManager()  # Default name 'mydama' assigned to the dictionary

    >>> dama.read_gwdata(e_gps - 50, e_gps +50, ifo='L1',          # Required params
                         m_data_source="gwosc-remote",             # data source
                         dts_key='online')                         # Optional but useful for giving names to things


From local CVMFS
----------------
 
CernVM-FS must be installed and configured on your computer. Refer to its `description on the GWOSC website <https://www.gw-openscience.org/cvmfs/>`_ 
or to `this Quick start guide <https://cernvm.cern.ch/portal/filesystem/quickstart>`_.

Assuming your data are stored at the following path:
::

   cvmfs_path = '/data2/cvmfs/gwosc.osgstorage.org/gwdata/' 

data can be read with:

::

    >>> start='2017-06-08 01:00:00'  # starting time
    >>> end='2017-06-08 02:00:00'    # ending time
    >>> ifo='H1'                     # which interfereometer

    >>> rate='4k'                    # determines the sample rate
    >>> frmt='hdf5'                  # and the format of the data (gwf or hdf5)
    
    >>> dama.read_gwdata(start, end, m_data_source="gwosc-cvmfs", ifo=ifo, m_data_format=frmt)