import enum
import random
import uuid
from decimal import Decimal


def random_str(prefix='', suffix='', length=8) -> str:
    """
    随机字符串(最大32位)
    :param prefix: 前缀
    :param suffix: 后缀
    :param length: 字符串长度
    :return: 随机字符串
    """
    return prefix + uuid.uuid4().__str__().replace('-', '')[:length] + suffix


def random_int(n, m) -> int:
    """
    随机生成n到m间的整数(包含n和m)
    :param n: 最小值
    :param m: 最大值
    :return: 随机整数
    """
    return random.randint(n, m)


def random_float(precision=0.00) -> Decimal:
    """
    随机生成浮点数，默认四舍五入保留小数点后两位
    :param precision: 精度
    :return: 随机浮点数
    """
    return Decimal(random.random()).quantize(Decimal(precision))


def float_scale(float_num, precision='0.00', scale=False):
    """
    浮点数保留小数点(默认不进位)
    :param float_num: 浮点数
    :param precision: 进位位数
    :param scale: 是否四舍五入
    :return: 浮点数保留小数点
    """
    if scale:
        return Decimal(float_num).quantize(Decimal(precision))

    else:
        a, b = str(float_num).split('.')
        return float(a + '.' + b[:precision.split('.')[1].__len__()])


def random_bool() -> bool:
    """
    随机布尔
    :return:
    """
    return bool(random_int(0, 1))


def random_list(array: list):
    """
    随机从list中取一个值
    :param array:
    :return:
    """
    return array[random_int(0, array.__len__() - 1)]


def random_enum(e: enum.EnumMeta) -> enum.EnumMeta:
    """
    随机从枚举中取一个值
    :param e:
    :return:
    """
    return random_list(list(e.__iter__()))
