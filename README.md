ibweb
=====

An Interactive Broker web viewer in python

For the moment, it use mongodb with pymongo (http://api.mongodb.org/python/current/).
In the future, I'll maybe implement a database abstraction.

IbPy
-----
It is base on IbPy library (http://code.google.com/p/ibpy) which is basicaly a java2python translation.
As the library is not maintained anymore, I applied a couple of patch to the latest stable version.
You will find this patched version in ./ibpy. To install the library, simply do "python setup.py install" (as root)

Modifications:
- ib.ext.Contract.Contract.__eq fix (Raised exception when no comboleg defined)
- ib.ext.Contract fix, Error not defined
- ib.ext.EClientSocket.py fix, crashed on TWS disconnect
- Add missing TickType in ib.ext.TickType.TickType
- Some small fixes
