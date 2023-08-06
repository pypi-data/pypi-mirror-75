================
RBD iSCSI Client
================


.. image:: https://img.shields.io/pypi/v/rbd-iscsi-client.svg
        :target: https://pypi.python.org/pypi/rbd-iscsi-client

.. image:: https://img.shields.io/travis/hemna/rbd-iscsi-client.svg
        :target: https://travis-ci.com/hemna/rbd-iscsi-client

.. image:: https://readthedocs.org/projects/rbd-iscsi-client/badge/?version=latest
        :target: https://rbd-iscsi-client.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/hemna/rbd-iscsi-client/shield.svg
     :target: https://pyup.io/repos/github/hemna/rbd-iscsi-client/
     :alt: Updates



This is a REST client that talks to ceph-iscsi's rbd-target-api to export
rbd images/volumes to an iSCSI initiator.


* Free software: Apache Software License 2.0
* Documentation: https://rbd-iscsi-client.readthedocs.io.


Overview
--------
This python package is a client that talks to the ceph-iscsi rbd-target-api.
rbd-target-api coordinates the rbd volume exports via iSCSI

Requirements
------------
This package requires a running ceph cluster that has the ceph-iscsi
gateway tools installed properly and running.  The rbd-target-api must
be configured and running

Installation
------------
``pip install rbd-iscsi-client``

Features
--------

This is a REST client that talks to ceph-iscsi's rbd-target-api to export
rbd images/volumes to an iSCSI initiator.

* get_api - Get all the api endpoints
* get_config - get the entire gateway config
* get_targets - Get all of the target_iqn's defined in the gateways
* create_target_iqn - create a new target_iqn
* delete_target_iqn - delete a target_iqn
* get_clients - get the clients (initiators) defined in the gateways
* get_client_info - get the client information
* create_client - Register a new client (initiator) with the gateways
* delete_client - unregister a client (initiator) from the gateways
* set_client_auth - set CHAP credentials for the client (initiator)
* get_disks - get list of volumes defined to the gateways
* create_disk - create a new volume/disk that the gateways can export
* find_disk - Find a disk that the gateway knows about
* delete_disk - delete a disk from the gateway and pool
* register_disk - Make the disk available to export to a client.
* unregister_disk - Make a disk unavailable to export to a client.
* export_disk - Export a registered disk to a client (initiator)
* unexport_disk - unexport a disk from a client (initiator)

Credits
-------

This package makes use of the rbd-target-api from ceph-iscsi_ package.

.. _ceph-iscsi: https://github.com/ceph/ceph-iscsi

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
