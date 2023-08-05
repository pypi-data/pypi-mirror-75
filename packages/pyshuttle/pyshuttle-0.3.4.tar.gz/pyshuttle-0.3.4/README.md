# Shuttle

[![Build Status](https://travis-ci.org/meherett/shuttle.svg?branch=master)](https://travis-ci.org/meherett/shuttle?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/pyshuttle.svg?color=blue)](https://pypi.org/project/pyshuttle)
[![Documentation Status](https://readthedocs.org/projects/shuttle/badge/?version=latest)](https://shuttle.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/meherett/shuttle/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/meherett/shuttle?branch=master)

Shuttle is a python library for cross-chain atomic swaps between the networks of two cryptocurrencies. Cross-chain atomic swaps are the cheapest and most secure way to swap cryptocurrencies. It’s a brand new decentralized payment environment based on Hash Time Lock Contracts (HTLCs) protocol. [Documentation](https://shuttle.readthedocs.io)

## Available Cryptocurrencies

Shuttle has the following available cryptocurrencies to swap:

| Cryptocurrencies                                        | Mainnet | Testnet | Solonet | 
| ------------------------------------------------------- | :-----: | :-----: | :-----: |
| [Bitcoin](https://github.com/bitcoin/bitcoin) `BTC`     | Yes     | Yes     | None    |
| [Bytom](https://github.com/bytom/bytom) `BTM`, `Assets` | Yes     | No      | No      |

## Dependencies

* [bytom-wallet-desktop](https://bytom.io/en/wallet/) - version [1.1.0](https://github.com/Bytom/bytom/releases/tag/v1.1.0) or greater.
* [pip](https://pypi.org/project/pip/) - To install packages from the Python Package Index and other indexes.
* [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater.

## Installation

PIP to install shuttle globally. For Linux sudo may be required.

```
$ pip install pyshuttle
```

For the versions available, see the [tags on this repository](https://github.com/meherett/shuttle/tags).

## Development

We welcome pull requests. To get started, just fork this repo, clone it locally, and run:

```
$ pip install -e .[tests] -r requirements.txt
```

## Testing

Tests are still under development.

You can run the tests with:

```
$ pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Contributing

Feel free to open an issue if you find a problem, or a pull request if you've solved an issue.

## License

Distributed under the [AGPL-3.0](https://github.com/meherett/shuttle/blob/master/LICENSE) license. See ``LICENSE`` for more information.
