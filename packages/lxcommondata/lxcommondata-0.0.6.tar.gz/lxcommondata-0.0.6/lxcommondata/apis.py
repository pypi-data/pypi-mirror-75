import json

from . import commondata_pb2, commondata_pb2_grpc
from .client import Client

con = Client.get_conn()

# 调用 rpc 服务
db_interface_stub = commondata_pb2_grpc.DBInterfaceStub(con)

def do_query(query_obj):
    """
    :param query_json:
    :return: status, data
    """
    query_json = json.dumps(query_obj)
    ret = db_interface_stub.query_db(commondata_pb2.query_params(params=query_json))
    ret_data = json.loads(ret.data)

    status = ret_data['status']
    data = json.loads(ret_data['data_json'])
   
    return status, data


func_interface_stub = commondata_pb2_grpc.FuncInterfaceStub(con)

def run_func(*args, **kwargs):

    params = {'args': args, 'kwargs': kwargs}
    params_json = json.dumps(params)

    ret = func_interface_stub.run_func(commondata_pb2.func_params(params=params_json))
    ret_data = json.loads(ret.data)

    status = ret_data['status']
    data = json.loads(ret_data['data_json'])

    return status, data