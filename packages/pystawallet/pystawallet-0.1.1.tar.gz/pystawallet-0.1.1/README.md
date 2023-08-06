# pystawallet

Python Stawallet Api Client

[![Build Status](https://travis-ci.org/stawallet/pystawallet.svg?branch=master)](https://travis-ci.org/stawallet/pystawallet)
[![Build Status](https://badge.fury.io/py/pystawallet.svg)](https://pypi.org/project/pystawallet/)
[![Build Status](https://pypip.in/d/pystawallet/badge.png)](https://pypi.org/project/pystawallet/)
[![codecov](https://codecov.io/gh/stawallet/pystawallet/branch/master/graph/badge.svg)](https://codecov.io/gh/stawallet/pystawallet)


Install using pypi:
```shell script
pip install pystawallet
```

## Stawallet
Home Page: https://stawallet.io/  
Api Doc: https://apidocs.stawallet.io/  
Sandbox Dashboard Url: https://sapp.stawallet.io/
Mainnet Dashboard Url: https://app.stawallet.io/

## Usage
Initialize api client:
```python
from pystawallet import StawalletApiClient

api_client = StawalletApiClient(api_key='MY-API-KEY', api_secret='MY-API-SECRET')
```

