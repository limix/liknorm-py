# liknorm-py

[![Travis](https://img.shields.io/travis/limix/liknorm-py.svg?style=flat-square&label=linux%20%2F%20macos%20build)](https://travis-ci.org/limix/liknorm-py) [![AppVeyor](https://img.shields.io/appveyor/ci/Horta/liknorm-py.svg?style=flat-square&label=windows%20build)](https://ci.appveyor.com/project/Horta/liknorm-py)

Liknorm Python wrapper.

## Install

The recommended way of installing it is via conda_

```bash
conda install -c conda-forge liknorm-py
```

An alternative way would be via [pip](https://pypi.python.org/pypi/pip).
First you need to install [liknorm](http://liknorm.readthedocs.io/) library and then

```bash
pip install liknorm-py
```

## Running the tests

After installation, you can test it

```bash
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
>>>
>>> print('%.3f %.3f %.3f' % (log_zeroth[0], mean[0], variance[0]))
-0.671 -0.515 0.946
```

## Authors

* [Danilo Horta](https://github.com/horta)

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/limix/liknorm-py/master/LICENSE.md).
