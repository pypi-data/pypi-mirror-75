================
CompressedLogger
================


.. image:: https://img.shields.io/pypi/v/compressedlogger.svg
        :target: https://pypi.python.org/pypi/compressedlogger


This is a logging handler to be used with the standard `python logging <https://docs.python.org/3/library/logging.html>`_ module. 
The handler compresses the \*.log logfiles directly into a \*.gz archive without writing an uncompressed file. You can choose the maximum size of 
a single \*.gz file and the overall maximum size of all compressed logs. This allows you to limit the diskspace usage of your logs directly in the handler. 
You can also set a `header` string which will be written at the beginning of every new log file.


Behaviour:
----------

* Once the file size of the current log reaches the maximum size it gets rotated
* Once the file sizes of all written logs together exceed the overall maximum size, the oldest logs will be deleted
* If a `header` was given, it will be written at the beginning of every log file
* The current logfile automatically rotates on date change
* \*.gz archives are named: foo.log-2020-07-15.1.gz, foo.log-2020-07-15.2.gz,...

The size limits are not completely strict. Each gzip file will be slightly larger than the maximum size since a gzip file needs to be flushed before closing it, which always adds some more bytes.
E.g., when the limit is set to 1 MB, the actual filesize of a compressed log will be around 1.1 MB.



Usage:
------

There are five parameters:

* log_path (str): path to the folder where the logs should be stored
* filename (str): the base name of the logfile mylog
* single_max_size (int): the maximum size of a single \*.gz file in megabytes
* overall_size (int): the maximum size of all \*.gz files in megabytes
* header (str): optional header that is written at the beginning of every logfile

.. code-block:: python

   compressed_handler = CompressedLogger(log_path="logs/", 
                                         filename="foolog.log",
                                         header="----- version: 1.0.32 -----",
                                         single_max_size=1,
                                         overall_size=5)





Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage