import enum


class Separator(enum.Enum):
    """
    分隔符
    """
    DOT = "."
    STAR = "*"
    L_STR = "|"


class JsonPath(object):
    """
    json路径解析
    """
    __ROOT = "$"
    __SQUARE_L = "["
    __SQUARE_R = "]"

    def __init__(self, json=None, separator=Separator.DOT, not_key_raise=True):
        self.json = json
        self.separator = separator.value
        self.not_key_raise = not_key_raise

    def path(self, path: str, json=None):
        """
        解析路径
        :param path: 路径表达式
        :param json: json字典
        :return:
        """
        if json is None:
            json = self.json

        if not path.startswith(self.__ROOT):
            raise SyntaxError("path: %s must start with '$'" % path)

        if path.count(self.__ROOT) != 1:
            raise SyntaxError("path: %s must contains one '$'" % path)

        for i in path.split(self.separator):
            if self.__ROOT in i:
                continue

            if self.__SQUARE_L in i:
                try:
                    json = self.__get(json, i.split(self.__SQUARE_L)[0])[
                        int(i[i.index(self.__SQUARE_L) + 1: i.index(self.__SQUARE_R)])]
                    continue
                except IndexError:
                    raise IndexError("list: %s index out of range, length: %d, index: %d" % (
                        self.__get(json, i.split(self.__SQUARE_L)[0]),
                        i.split(self.__SQUARE_L)[0].__len__(),
                        int(i[i.index(self.__SQUARE_L) + 1: i.index(self.__SQUARE_R)])))
                except Exception as e:
                    raise Exception(e)

            json = self.__get(json, i)

        return json

    def __get(self, json, key: str):
        if isinstance(json, dict):
            if key not in json.keys():
                if self.not_key_raise:
                    raise Exception("json: %s have not key: %s" % (json, key))
                else:
                    return None
            return json.get(key)

        if isinstance(json, list):
            return json

        raise Exception("Can't find key: %s in primary value: %s" % (key, json))


if __name__ == '__main__':
    _json_dict = {'k': 'v'}
    _jp1 = JsonPath(_json_dict)
    assert _jp1.path("$.k") == 'v'

    _json_list = [{'k': 'v'}]
    _jp2 = JsonPath(_json_list)
    assert _jp2.path("$.[0].k") == 'v'

    _json_complex = {'k': [{'k': 'v'}]}
    _jp3 = JsonPath(_json_complex)

    assert _jp3.path("$.k.[0].k") == 'v'

    _jp4 = JsonPath(_json_dict)
    assert _jp4.path("$.[0].k", [{'k': 'v'}]) == 'v'

    _jp5 = JsonPath(_json_dict, not_key_raise=False)
    assert _jp5.path('$.m') == None

