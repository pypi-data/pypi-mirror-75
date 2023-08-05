import json
from functools import wraps

import aiohttp.web
import aiohttp.web_request

from aiojson.exception import ApiException
from aiojson.response import GoodResponse, BadResponse


class WrongDataType(ApiException):
    text = "Wrong data type."

    def __init__(self, path):
        super().__init__({
            "text": self.text,
            "path": path,
        })


class DataMissing(ApiException):
    text = "Required data is missing."

    def __init__(self, path):
        super().__init__({
            "text": self.text,
            "path": path,
        })


class UnknownFields(ApiException):
    text = "Unknown fields."

    def __init__(self, fields):
        super().__init__({
            "text": self.text,
            "path": fields,
        })


class JsonTemplate:
    def __init__(self, template: dict = None,
                 ignore_unknown=True):
        self.validate_template(template)
        self.template: dict = template if template else {}
        self.ignore_unknown = ignore_unknown

    @staticmethod
    def get_required(template):
        required_list = template.pop("__required__", [])
        if "__all__" in required_list:
            required_list.remove("__all__")
            for key in template.keys():
                required_list.append(key)
        return required_list

    def __call__(self, func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            try:
                request = None
                for arg in args:
                    if isinstance(arg, aiohttp.web_request.Request):
                        request = arg
                validated_data = {}
                if await request.read():
                    validated_data = self.validate_data(await request.json(),
                                                        self.template.copy())
                elif self.template.get("__required__"):
                    raise DataMissing(self.template["__required__"])
                result = await func(*args, validated_data=validated_data, **kwargs)
                if isinstance(result, aiohttp.web.Response):
                    return result
                return GoodResponse(result)
            except ApiException as e:
                return BadResponse(e.message, e.status)
            except json.decoder.JSONDecodeError:
                return BadResponse("Wrong json data format")
        return wrap

    def validate_template(self, template):
        """Validates template"""

    def validate_data(self, data, template, path=""):
        data = data.copy()
        validated_data = {}
        required = self.get_required(template)
        template = {k: v for k, v in template.items() if not k.startswith("__")}
        if set(data).difference(template) and not self.ignore_unknown:
            raise UnknownFields(list(set(data).difference(template)))
        for key, sub_template in template.items():
            is_required = key in required
            try:
                if not data.get(key) and is_required:
                    raise DataMissing(f"{path}.{key}" if path else key)
                elif not data.get(key) and not is_required:
                    continue

                if isinstance(sub_template, type):
                    validated_data[key] = sub_template(data[key])
                elif isinstance(sub_template, dict) and isinstance(data.get(key), dict):
                    validated_data[key] = self.validate_data(data[key], sub_template,
                                                             f"{path}.{key}" if path else key)
                elif isinstance(sub_template, list) and isinstance(data.get(key), list):

                    validated_data[key] = self.validate_list(data[key], sub_template,
                                                             f"{path}.{key}" if path else key)
                else:
                    raise WrongDataType(f"{path}.{key}" if path else key)
            except TypeError:
                raise WrongDataType(f"{path}.{key}" if path else key)
            except ValueError:
                raise WrongDataType(f"{path}.{key}" if path else key)
        return validated_data

    def validate_list(self, data, template, path):
        template = template[0]
        validated_data = []
        if isinstance(template, type):
            for n, item in enumerate(data):
                try:
                    validated_data.append(template(item))
                except ValueError:
                    raise WrongDataType(f"{path}.{n}" if path else n)
        elif isinstance(template, dict):
            for n, item in enumerate(data):
                validated_data.append(self.validate_data(item, template,
                                                         f"{path}.{n}" if path else n))
        return validated_data
