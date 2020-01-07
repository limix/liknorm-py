# liknorm-py

[![Travis](https://travis-ci.com/limix/liknorm-py.svg?branch=master)](https://travis-ci.com/limix/liknorm-py)

Liknorm Python wrapper.

## Install

It can be done via [pip](https://pypi.org/) or [conda](https://conda.io/).

### Pip

```bash
pip install liknorm
```

### Conda

```bash
conda install -c conda-forge liknorm-py
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

This project is licensed under the
[MIT License](https://raw.githubusercontent.com/limix/liknorm-py/master/LICENSE.md).
