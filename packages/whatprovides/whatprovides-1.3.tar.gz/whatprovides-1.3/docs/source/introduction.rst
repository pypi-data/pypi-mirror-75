**whatprovides** is a package that allows you to search for python modules that contain declared classes,
functions and variables by the name of the search object.

This is an analogue of the **yum whatprovides** command in **Centos**.

Search is performed in the current active virtual environment.

For example:

 .. code-block:: bash

  whatprovides.py ArgumentParser

Will return something like this:

  class: ArgumentParser: /usr/lib/python3.7/argparse.py

