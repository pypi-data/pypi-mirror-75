pybt
====

|Build Status|

|asciicast|

.. _how-to-:

how to ...
----------

.. _-get-started:

... get started
~~~~~~~~~~~~~~~

.. code:: shell

   ./dependencies.py

.. _-to-use-it:

... to use it
~~~~~~~~~~~~~

::

   Python 3.7.5rc1 (default, Oct  8 2019, 16:47:45)
   Type 'copyright', 'credits' or 'license' for more information
   IPython 7.9.0 -- An enhanced Interactive Python. Type '?' for help.

   In [1]: from pybt import Scanner, ClassicDevice

   In [2]: Scanner.scan_for()
   Permission Denied
   Set scan parameters failed (are you root?)
   found 1 devices
   Out[2]: [<pybt.libs.bt.classic.ClassicDevice at 0x7f3427045210>]

   In [3]: c = ClassicDevice.scan()

   In [4]: c
   Out[4]: [<pybt.libs.bt.classic.ClassicDevice at 0x7f3425559d50>]

   In [5]: c[0].__dict__
   Out[5]:
   {'address': 'A8:B8:6E:C1:6A:28',
    'timestamp': '03.11.2019 16:48:06',
    'name': 'Nexus 5X'}

or check `bt.py`_

.. _bt.py: https://github.com/smthnspcl/pybt/blob/master/bt.py

.. |Build Status| image:: https://build.eberlein.io/buildStatus/icon?job=python_pybt
   :target: https://build.eberlein.io/job/python_pybt/
.. |asciicast| image:: https://asciinema.org/a/299826.svg
   :target: https://asciinema.org/a/299826