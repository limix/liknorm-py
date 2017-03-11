# liknorm-py

[![PyPIl](https://img.shields.io/pypi/l/liknorm-py.svg?style=flat-square)](https://pypi.python.org/pypi/liknorm-py/)
[![PyPIv](https://img.shields.io/pypi/v/liknorm-py.svg?style=flat-square)](https://pypi.python.org/pypi/liknorm-py/)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/liknorm-py/badges/version.svg)](https://anaconda.org/conda-forge/liknorm-py)

Liknorm Python wrapper.

## Install

The recommended way of installing it is via
[conda](http://conda.pydata.org/docs/index.html)
```bash
conda install -c conda-forge liknorm-py
```

An alternative way would be via [pip](https://pypi.python.org/pypi/pip).
First you need to install [liknorm](http://liknorm.readthedocs.io/en/latest/)
library and then
```bash
pip install liknorm-py
```

## Running the tests

After installation, you can test it
```
python -c "import liknorm; liknorm.test()"
```
as long as you have [pytest](http://docs.pytest.org/en/latest/).

## Example

```python
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
>>> print('%.3f %.3f %.3f' % (log_zeroth[0], mean[0], variance[0]))
-0.671 -0.515 0.946
```

## Authors

* **Danilo Horta** - [https://github.com/Horta](https://github.com/Horta)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details
