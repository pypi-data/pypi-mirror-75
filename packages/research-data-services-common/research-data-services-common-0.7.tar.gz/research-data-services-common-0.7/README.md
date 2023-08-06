[![Maintainability](https://api.codeclimate.com/v1/badges/002a567a70219a941a2f/maintainability)](https://codeclimate.com/github/Sciebo-RDS/py-research-data-services-common/maintainability)[![Test Coverage](https://api.codeclimate.com/v1/badges/002a567a70219a941a2f/test_coverage)](https://codeclimate.com/github/Sciebo-RDS/py-research-data-services-common/test_coverage)[![PyPI version](https://badge.fury.io/py/research-data-services-common.svg)](https://badge.fury.io/py/research-data-services-common)

# Research Data Services Common Package

This package make the most common modules in Sciebo RDS available in one place, so we do not have to maintain them in several places.
In the RDS project, we use OAuth2 for authentication between numerious services, so we need a datastructure with methods, which supports this.

So this package implement 3 basic classes (User, Service, Token), which handles standard user-password authentication.
If you need this classes with oauth2-support, you have to use the corresponding version (e.g. Service => Oauth2Service). (Notice: User does not have an oauth2-version, because token takes care of password or token and service takes care of everything else for oauth2.)

## Usage

You can find some examples to use this package below. If you need more, please take a look into the tests or [sciebo RDS](https://github.com/Sciebo-RDS/Sciebo-RDS) (e.g. [Token Storage](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/circle3_central_services/token_storage/src/lib/Storage.py)).

```python
from RDS import User
user1 = User("Max Mustermann")
```

## Installation

```bash
pip install research-data-services-common
```

### Optional dependencies

If you want to work with flask, you can use some additional features, when it is installed.

```bash
pip install "research-data-services-common[flask]"
```

## JSONEncoder

With flask installed, you can use the JSONEncoder for flask.

```python
from flask import Flask, jsonify
from RDS import Util

app = Flask(__name__)
app.json_encoder = Util.get_encoder(func_name="to_dict")

class Storage():
    def to_dict(self):
        return {"foo": "bar"}

@app.route("/")
def hello():
    return jsonify(Storage())
```

If you want to use builtin json, you do not need flask. Then you can use *monkeypatch*-method.

```python
from RDS import Util
import json

class Storage():
    def to_dict(self):
        return {"foo": "bar"}

Util.monkeypatch(func_name="to_dict")

print(json.dumps(Storage())) # expects: '{"foo":"bar"}'
```

**Notice**: func_name defaults to *to_json*.

## Available Modules

- User
- Service (Oauth2Service)
- Token (Oauth2Token)
