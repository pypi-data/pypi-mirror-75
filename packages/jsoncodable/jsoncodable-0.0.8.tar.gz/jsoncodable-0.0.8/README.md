# jsoncodable
![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/jsoncodable?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/jsoncodable)


<p align="center">
  <img src="https://i.imgur.com/F8TfIYt.png" />
</p>

## Description
Easily create object from any dict and dict from any object

## Install
~~~~shell
pip install jsoncodable
# or
pip3 install jsoncodable
~~~~

## Usage
~~~~python
from jsoncodable import *
import json

# ---------------------------------------- Any object to json dict ---------------------------------------- #

class Test1:
    def __init__(self, value: int):
        self.value1 = value
        self.value2 = value * 2
        self.values = [self.value1, self.value2]

class Test2(JSONCodable):
    def __init__(self, value: int):
        self.test1 = Test1(value)

test2 = Test2(5)
print(test2.dict)
# prints:
# 
# {'test1': <__main__.Test1 object at 0x1018199d0>}

print(json.dumps(test2.json, indent=4))
# or
test2.jsonprint()
#
# both will print:
# 
# {
#     "test1": {
#         "value1": 5,
#         "value2": 10,
#         "values": [
#             5,
#             10
#         ]
#     }
# }

# ---------------------------------------- Any json dict to object ---------------------------------------- #

class Test3(JSONCodable):
    pass

json_str = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

print(Test3.from_json(json_str))
# prints:
# 
# JSONCodable(name='John Smith', hometown=JSONCodable(name='New York', id=123))

print(Test3.from_json(json.loads(json_str)))
# prints:
# 
# JSONCodable(name='John Smith', hometown=JSONCodable(name='New York', id=123))
~~~~
