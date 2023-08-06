import grpc

from django.conf import settings


class Client:

    conn = None

    @classmethod
    def connect(cls, server):
        """
        # 连接 rpc 服务器
        :param server:
        :return:
        """

        cls.conn = grpc.insecure_channel(server)

    @classmethod
    def get_conn(cls):
        return cls.conn


server = settings.COMMON_DATA_SERVER

Client.connect(server)