import sys
from .apis import run_func

def get_nic(c, m="name"):
    """
    根据编码获取行业全名
    :param c:
    :param m:
    :return:
    """

    status, ret = run_func(c, m=m, func=sys._getframe().f_code.co_name)
    return ret

