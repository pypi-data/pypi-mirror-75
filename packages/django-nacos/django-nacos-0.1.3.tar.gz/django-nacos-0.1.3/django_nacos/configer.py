import nacos
from django.conf import settings


def client(namespace: str = None):
    """client 获取nacos客户端
    需配置settings.NACOS = dict(servers='a,b', namespace='namespace id', ak='username', sk='password')

    :param namespace: 命名空间id, defaults to None
    :type namespace: str, optional
    """

    servers = settings.NACOS["servers"]
    namespace = namespace or settings.NACOS["namespace"]
    ak = settings.NACOS["ak"]
    sk = settings.NACOS["sk"]
    return nacos.NacosClient(servers, namespace=namespace, ak=ak, sk=sk)
