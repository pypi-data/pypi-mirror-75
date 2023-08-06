import argparse
from typing import List


class Arg:
    """
    参数
    name or flags - 一个命名或者一个选项字符串的列表，例如 foo 或 -f, --foo。
    action - 当参数在命令行中出现时使用的动作基本类型。
    nargs - 命令行参数应当消耗的数目。
    const - 被一些 action 和 nargs 选择所需求的常数。
    default - 当参数未在命令行中出现时使用的值。
    type - 命令行参数应当被转换成的类型。
    choices - 可用的参数的容器。
    required - 此命令行选项是否可省略 （仅选项可用）。
    help - 一个此选项作用的简单描述。
    metavar - 在使用方法消息中使用的参数值示例。
    dest - 被添加到 parse_args() 所返回对象上的属性名。
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Args:
    """
    参数集
    """
    def __init__(self, args: List[Arg], name, desc=''):
        self.args = args
        self.name = name
        self.desc = desc

    def parse(self) -> argparse.Namespace:
        """
        解析控制台输入的参数
        :return:
        """
        parser = argparse.ArgumentParser(prog=self.name, description=self.desc)

        for arg in self.args:
            parser.add_argument(*arg.args, **arg.kwargs)

        return parser.parse_args()


if __name__ == '__main__':
    args = Args(
        name='args-demo',
        args=[
            Arg('-c', '--config', help='配置文件路径', default='config.yaml'),
            Arg('-f', '--file', help='csv文件路径', required=False),
            Arg('-w', action='store_true')
        ],
        desc='Args Demo desc'
    ).parse()
