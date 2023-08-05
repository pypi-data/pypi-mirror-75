# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Dict, Any
import json

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: JsonCodable ---------------------------------------------------------- #

class JSONCodable:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @classmethod
    def from_json(cls, json_data: Any) -> Optional:
        try:
            from collections import namedtuple

            if not isinstance(json_data, str):
                json_data = json.dumps(json_data)

            return json.loads(json_data, object_hook=lambda d: namedtuple('JSONCodable', d.keys())(*d.values()))
        except Exception as e:
            print(e)

            return None
    
    @classmethod
    def from_json_file(cls, json_file_path: Any) -> Optional:
        try:
            with open(json_file_path, 'r') as f:
                return cls.from_json(json.load(f))
        except Exception as e:
            print(e)

            return None
    
    # alias
    load = from_json_file

    @property
    def dict(self) -> Dict:
        '''Creates, dict from object.'''
        return self.to_dict(self, recursive=False)

    @property
    def json(self) -> Dict:
        '''Same as .dict, but converts all object values to JSONSerializable ones recursively'''
        return self.to_dict(self, recursive=True)


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def save_to_file(self, path: str, indent: int=4):
        with open(path, 'w') as f:
            json.dump(self.json, f, indent=indent)

    # alias
    save = save_to_file

    def jsonprint(self) -> None:
        print(json.dumps(self.json, indent=4))

    @classmethod
    def to_dict(cls, obj: Optional[Any], recursive: bool=True) -> Optional[Dict]:
        if obj is None or type(obj) in [str, float, int, bool]:
            return obj

        from copy import deepcopy
        from enum import Enum

        obj = deepcopy(obj)

        if isinstance(obj, list) or isinstance(obj, tuple):
            v_list = []

            for vv in obj:
                v_list.append(cls.to_dict(vv, recursive=recursive))

            return v_list
        elif isinstance(obj, dict):
            v_dict = {}

            for k, vv in obj.items():
                v_dict[k] = cls.to_dict(vv, recursive=recursive)

            return v_dict
        elif issubclass(type(obj), Enum):
            return obj.value

        real_dict = cls.__real__dict__(obj)

        return real_dict if not recursive else cls.to_dict(real_dict, recursive=recursive)

    @staticmethod
    def __real__dict__(obj, include_private: bool = False) -> Dict[str, Any]:
        object_dict = {}

        for method_name in [method_name for method_name in dir(obj)]:
            if (
                (
                    not include_private and method_name.startswith('_')
                )
                or
                (
                    method_name in dir(JSONCodable())
                )
                or
                (
                    callable(getattr(obj, method_name))
                )
            ):
                continue

            object_dict[method_name] = getattr(obj, method_name)

        return object_dict


# ---------------------------------------------------------------------------------------------------------------------------------------- #