QSCOUT Gate Models
------------------

The [Quantum Scientific Computing Open User Testbed
(QSCOUT)](https://qscout.sandia.gov/) is a five-year DOE program to build a
quantum testbed based on trapped ions that is available to the research
community. As an open platform, it will not only provide full specifications
and control for the realization of all high level quantum and classical
processes, it will also enable researchers to investigate, alter, and optimize
the internals of the testbed and test more advanced implementations of quantum
operations.

This Python package allows [JaqalPaq](https://gitlab.com/jaqal/jaqalpaq)
to understand the native gate set used by QSCOUT hardware.  In particular,
it allows JaqalPaq to emulate Jaqal programs targeting QSCOUT hardware.

## Installation

The QSCOUT Gate Models package is available on
[GitLab](https://gitlab.com/jaqal/qscout-gatemodels).
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install it.

```bash
pip install qscout-gatemodels
```

[pyGSTi](https://www.pygsti.info/) is used to perform forward simulations, and
is a recommended dependency.

```bash
pip install pygsti
```

## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

## Questions?

For help and support, please contact
[qscout@sandia.gov](mailto:qscout@sandia.gov).
