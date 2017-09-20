
liknorm-py
==========

|PyPI-Status| |Conda-Forge-Status| |Conda-Downloads|

|Build-Status| |Codacy-Grade| |License-Badge|

Liknorm Python wrapper.

Install
-------

The recommended way of installing it is via conda_

.. code:: bash

    conda install -c conda-forge liknorm-py

An alternative way would be via pip_.
First you need to install liknorm_ library and then

.. code:: bash

    pip install liknorm-py

Running the tests
-----------------

After installation, you can test it

.. code:: bash

    python -c "import liknorm; liknorm.test()"

as long as you have pytest_.

Example
-------

.. code:: python

    >>> from numpy import empty
    >>> from numpy.random import RandomState
    >>> from liknorm import LikNormMachine
    >>>
    >>> machine = LikNormMachine('bernoulli')
    >>> random = RandomState(0)
    >>> outcome = random.randint(0, 2, 5)
    >>> tau = random.rand(5)
    >>> eta = random.randn(5) * tau
    >>>
    >>> log_zeroth = empty(5)
    >>> mean = empty(5)
    >>> variance = empty(5)
    >>>
    >>> moments = {'log_zeroth': log_zeroth, 'mean': mean, 'variance': variance}
    >>> machine.moments(outcome, eta, tau, moments)
    >>>
    >>> print('%.3f %.3f %.3f' % (log_zeroth[0], mean[0], variance[0]))
    -0.671 -0.515 0.946

Authors
-------

* `Danilo Horta`_

License
-------

This project is licensed under the MIT License - see the `license file`_ for
details.

.. |Build-Status| image:: https://travis-ci.org/limix/liknorm-py.svg?branch=master
    :target: https://travis-ci.org/limix/liknorm-py

.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/c13a6a45773e41d9bc4e3b1c679b3b96
    :target: https://www.codacy.com/app/danilo.horta/liknorm-py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=limix/liknorm-py&amp;utm_campaign=Badge_Grade

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/liknorm-py.svg
    :target: https://pypi.python.org/pypi/liknorm-py

.. |Conda-Forge-Status| image:: https://anaconda.org/conda-forge/liknorm-py/badges/version.svg
    :target: https://anaconda.org/conda-forge/liknorm-py

.. |Conda-Downloads| image:: https://anaconda.org/conda-forge/liknorm-py/badges/downloads.svg
    :target: https://anaconda.org/conda-forge/liknorm-py

.. |License-Badge| image:: https://img.shields.io/pypi/l/liknorm-py.svg
    :target: https://raw.githubusercontent.com/limix/liknorm-py/master/LICENSE.txt

.. _license file: https://raw.githubusercontent.com/limix/liknorm-py/master/LICENSE.txt

.. _Danilo Horta: https://github.com/horta

.. _conda: http://conda.pydata.org/docs/index.html

.. _pip: https://pypi.python.org/pypi/pip

.. _pytest: http://docs.pytest.org/en/latest/

.. _liknorm: http://liknorm.readthedocs.io/
