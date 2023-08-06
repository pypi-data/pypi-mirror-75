# GS PY Config

Configuration class

![Python package](https://github.com/guionardo/py-config/workflows/Python%20package/badge.svg)
[![codecov](https://codecov.io/gh/guionardo/py-config/branch/develop/graph/badge.svg)](https://codecov.io/gh/guionardo/py-config)


## Usage

Create your configuration class, extending config_guiosoft.ConfigClass

``` python
from config_guiosoft import ConfigClass
from datetime import datetime, time

class Config(ConfigClass):
  STRING_CONF = "DEFAULT VALUE"
  INT_CONF = 10
  FLOAT_CONF = 0.0
  BOOL_CONF = False  
  DATE = date.today()
  DATETIME = datetime.now()

config = Config()
print(config)
>>> __main__.Config(BOOL_CONF:False,DATE:datetime.date(2020, 7, 30),DATETIME:datetime.datetime(2020, 7, 30, 18, 39, 55, 374515),FLOAT_CONF:0.0,INT_CONF:10,STRING_CONF:'DEFAULT VALUE')
```

When this class is instantiated, it loads values from environment variables with same name.
If the variable is undefined, default values will be used.

## Advanced usage

You can use ConfigType for special field behavior.

``` python
from config_guiosoft import ConfigClass, ConfigType
from datetime import datetime, time

class SpecialConfig(ConfigClass):
    STRING_CONF = ConfigType(
        'STRING_CONF', str, 'DEFAULT_STRING', lambda value: len(value) > 1)
    INT_CONF = ConfigType(
        'INT_CONF', int, 100, range(1000))
    FLOAT_CONF = ConfigType(
        "FLOAT_CONF", float, 0.5, [0, 0.1, 0.5, 3.14])
    BOOL_CONF = ConfigType(
        "BOOL_CONF", bool, False)
    DEFAULT_CONF = ConfigType("DEFAULT_CONF")
    DATE = ConfigType(
        "DATE", date, date.today(), lambda value: value <= date.today())
    DATETIME = ConfigType(
        "DATETIME", datetime, datetime.now(),
        lambda value: value <= datetime.now())

# ConfigType constructor

ConfigType(env_name: str, type=str, default=None, validation: callable = None)

```
| Field | Description |
| ----- | ----------- |
| env_name | Environment variable name, string, required |
| type | python type (str, int, float, bool, datetime, date) |
| default | default value (must be compatible with type) |
| validation | callable to validate data|

