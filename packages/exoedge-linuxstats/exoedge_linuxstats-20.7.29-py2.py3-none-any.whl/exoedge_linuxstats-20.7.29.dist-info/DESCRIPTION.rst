Description
############

The purpose of this repository is to provide an ExoEdge protocol source that can report linux system information.

A protocol source (often just referred to as a "source") is the glue between ExoEdge and the field-bus that you want to get data to and from. It is helpful to think of a source as a plugin to ExoEdge.

.. image:: images/LinuxStatsConfig.png

Available Functions
"""""""""""""""""""""""
time
----
Displays the current time in the format "HH:MM:SS"

datetime
--------
Displays the current datetime of the device in the format "YYYY-MM-DD HH:MM:SS.sss"

cpu
---
Displays the current CPU usage as a percent

mem
---
Displays the current memory usage as a percent

interfaces
----------
Requires '/sbin/ifconfig' or 'ip a' to execute on the device.
Displays the active interfaces and their IP addresses in a JSON format. Use the 'JSON Table' panel to view.


Install
#########

Installing a build can be done in several ways:

Installing From Source
"""""""""""""""""""""""

.. code-block:: bash

    $ python setup.py install


Installing From Builds
"""""""""""""""""""""""

.. code-block:: bash

    $ pip install dist/*.whl


Installing From Builds
"""""""""""""""""""""""

.. code-block:: bash

    $ pip install exoedge_linuxstats


