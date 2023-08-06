datacoco-cloud
=================

.. image:: https://badge.fury.io/py/datacoco-cloud.svg
    :target: https://badge.fury.io/py/datacoco-cloud
    :alt: PyPI Version

.. image:: https://readthedocs.org/projects/datacococloud/badge/?version=latest
    :target: https://datacococloud.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/8b768d9639a94456b8574158122f36ae
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-cloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-cloud&amp;utm_campaign=Badge_Grade
    :alt: Code Quality Grade

.. image:: https://api.codacy.com/project/badge/Coverage/36df276fb1fe47d18ff1ea8c7a0aa522
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-cloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-cloud&amp;utm_campaign=Badge_Coverage
    :alt: Coverage

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
    :target: https://github.com/equinoxfitness/datacoco-cloud/blob/master/CODE_OF_CONDUCT.rst
    :alt: Code of Conduct

Datacoco-cloud contains interaction classes S3, Athena, SES, SNS, SQS, ECS, EMR, Cloudwatch logs

Installation
------------

datacoco-cloud requires Python 3.6+

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install datacoco-cloud

Quickstart
----------

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install --upgrade pip
    pip install -r requirements_dev.txt


Development
-----------

Getting Started
~~~~~~~~~~~~~~~

It is recommended to use the steps below to set up a virtual environment for development:

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install -r requirements.txt

Testing
~~~~~~~

::

    pip install -r requirements_dev.txt

To run the testing suite, simply run the command: ``tox`` or ``python -m unittest discover tests``

Contributing
------------

Contributions to datacoco\_cloud are welcome!

Please reference guidelines to help with setting up your development
environment
`here <https://github.com/equinoxfitness/datacoco-cloud/blob/master/CONTRIBUTING.rst>`__.