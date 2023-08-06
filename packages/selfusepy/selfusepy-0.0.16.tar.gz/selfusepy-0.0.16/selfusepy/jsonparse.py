#    Copyright 2018-2020 LuomingXu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Author : Luoming Xu
#   File Name : jsonparse.py
#   Repo: https://github.com/LuomingXu/selfusepy

"""
Json to Object的工具库
"""
from typing import MutableMapping, TypeVar

T = TypeVar('T')
class_dict = {}
__classname__: str = '__classname__'


class BaseJsonObject(object):
    """
    用于在用户自定义Json的转化目标类的基类
    以是否为此基类的子类来判断这个类是否需要转化
    """
    pass


class JsonField(object):

    def __init__(self, varname, ignore: bool = False, func = None):
        self.varname: str = varname  # object's var's name
        self.ignore: bool = ignore  # do not convert this field
        self.handle_func = func  # handle function for this variable


def DeserializeConfig(_map: MutableMapping[str, JsonField]):
    """
    :param _map: key->json key, value->annotation
    :return:
    """

    def func(clazz):
        def get_annotation(self, k: str = None) -> JsonField or MutableMapping[str, JsonField]:
            return _map.get(k) if k else _map

        clazz.get_annotation = get_annotation
        return clazz

    return func


"""
Archive
```python
def JSONField(key_variable: dict):
  def func(cls):
    @override_str
    class NoUseClass(BaseJsonObject):
      def __init__(self, *args, **kwargs):
        self = cls(*args, **kwargs)

      @classmethod
      def json_key_2_variable_name(cls, k: str):
        return key_variable.get(k)

    return NoUseClass

  return func
```
"""


def __deserialize_object__(d: dict) -> object or dict:
    """
    用于json.loads()函数中的object_hook参数
    :param d: json转化过程中的字典
    :return: object
    """
    cls_name = d.pop(__classname__, None)
    cls = class_dict.get(cls_name)
    if cls:
        obj = cls.__new__(cls)  # Make instance without calling __init__
        flag = hasattr(obj, 'get_annotation')
        for key, value in d.items():
            if flag:  # 判断是否有JSONField注解
                res: JsonField = obj.get_annotation(key)
                if res:  # 判断这个key是否配置了注解
                    if res.ignore:
                        continue
                    if res.varname is not None:
                        key = res.varname
                    if res.handle_func is not None:
                        value = res.handle_func(value)
            setattr(obj, key, value)
        return obj
    else:
        return d


def __add_classname__(d: dict, classname: str) -> dict:
    """
    给json字符串添加一个"__classname__"的key来作为转化的标志
    :param d: json的字典
    :param classname: 转化的目标类
    :return: 修改完后的json dict
    """
    d[__classname__] = classname
    for k, v in d.items():
        if isinstance(v, dict):
            __add_classname__(v, k.capitalize())
        elif isinstance(v, list):
            for item in v:
                # 如果这个list是基本类型(int, str...)之类则不需要添加classname
                if isinstance(item, int) or isinstance(item, str) or \
                    isinstance(item, bool) or \
                        isinstance(item, complex):
                    break
                __add_classname__(item, k.capitalize())

    return d


def __add_classname_list__(l: list, classname: str) -> list:
    for d in l:
        __add_classname__(d, classname)
    return l


def __generate_class_dict__(obj: BaseJsonObject):
    """
    构造需要转化的目标类的所包含的所有类
    将key: 类名, value: class存入class_dict中
    :param obj: 目标类
    """
    cls = type(obj)
    class_dict[cls.__name__] = cls
    for item in vars(obj).values():
        cls = type(item)
        if issubclass(cls, BaseJsonObject):
            __generate_class_dict__(cls())
        elif issubclass(cls, list):
            cls = type(item.pop(0))
            if issubclass(cls, BaseJsonObject):
                __generate_class_dict__(cls())
