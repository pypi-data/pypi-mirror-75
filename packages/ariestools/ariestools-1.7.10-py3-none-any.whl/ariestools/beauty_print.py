from typing import List


def bp_list(l: List):
    for i in l:
        print(i)


def bp_dict(d: dict):
    for k, v in d.items():
        print(k, v)