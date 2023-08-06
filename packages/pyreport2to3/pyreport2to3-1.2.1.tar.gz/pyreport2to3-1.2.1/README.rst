
This package helps in generating better visualization report in python 2 to 3.

Installation
------------

You can install directly after cloning:

use the Python package:

.. code-block:: bash

  $ pip install --user pyreport2to3

Command line tool
-----------------

After installation, you should have ``pyreport2to3`` in your ``$PATH``:


Usage
-----

Python porting 2 to 3 report function:

.. code-block:: python

    >>> from pyreport2to3 import get_HTMLreport


Call the get_HTMLreport function passing command (2to3 or python-modernize) and parameter (python folder or files) :

.. code-block:: python

    >>> get_HTMLreport("python-modernize", "./python_project")


Python porting 2 to 3 HTML file pyreporting.html is generated in current location.

License
~~~~~~~
MIT License
~~~~~~~~~~~


.. code:: rst

    |MIT license|

    .. image:: https://img.shields.io/badge/License-MIT-blue.svg

Authors
~~~~~~~
Maurya Allimuthu ( catchmaurya@gmail.com )
Jitendra Kumar
Abraham Robert ( abrahamrobert123@gmail.com )

Contact
~~~~~~~
Please submit an issue if you encounter a bug and please email any questions or requests to @authors