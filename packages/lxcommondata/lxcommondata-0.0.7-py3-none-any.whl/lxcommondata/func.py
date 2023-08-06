import sys
from .apis import run_func

def get_nic(c, m="name"):
    """
    根据编码获取行业全名
    :param c:
    :param m:
    :return:
    """

    status, data = run_func(c, m=m, func=sys._getframe().f_code.co_name)
    return data


def get_ent_nic(ent_id):
    """
    获取企业行业信息
    :param ent_id:
    :return:
    """
    status, data = run_func(ent_id, func=sys._getframe().f_code.co_name)
    return data


def get_ent_type(ent_type_id):
    """
    获取企业类型
    :param ent_type_id:
    :return:
    """
    status, data = run_func(ent_type_id, func=sys._getframe().f_code.co_name)
    return data