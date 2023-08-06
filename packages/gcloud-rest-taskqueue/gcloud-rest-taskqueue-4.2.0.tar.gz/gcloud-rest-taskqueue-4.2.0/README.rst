(Asyncio OR Threadsafe) Python Client for Google Cloud Task Queue
=================================================================

|pypi| |pythons-aio| |pythons-rest|

Installation
------------

.. code-block:: console

    $ pip install --upgrade gcloud-{aio,rest}-taskqueue

Usage
-----

We're still working on documentation -- for now, you can use the `smoke tests`_
as an example.

Emulators
~~~~~~~~~

For testing purposes, you may want to use ``gcloud-rest-taskqueue`` along with a
local emulator. Setting the ``$CLOUDTASKS_EMULATOR_HOST`` environment variable
to the address of your emulator should be enough to do the trick.

Contributing
------------

Please see our `contributing guide`_.

.. _contributing guide: https://github.com/talkiq/gcloud-rest/blob/master/.github/CONTRIBUTING.rst
.. _smoke tests: https://github.com/talkiq/gcloud-rest/tree/master/taskqueue/tests/integration

.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-rest-taskqueue.svg?style=flat-square
    :alt: Latest PyPI Version (gcloud-rest-taskqueue)
    :target: https://pypi.org/project/gcloud-rest-taskqueue/

.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-taskqueue.svg?style=flat-square&label=python (aio)
    :alt: Python Version Support (gcloud-rest-taskqueue)
    :target: https://pypi.org/project/gcloud-rest-taskqueue/

.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-taskqueue.svg?style=flat-square&label=python (rest)
    :alt: Python Version Support (gcloud-rest-taskqueue)
    :target: https://pypi.org/project/gcloud-rest-taskqueue/
