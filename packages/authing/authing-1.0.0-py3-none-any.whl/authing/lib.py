import jwt
import time
import rsa
import base64
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def getTokenInfo(token):
    return jwt.decode(token, verify=False)


def tokenExpCheck(token):
    """检测 Token 是否过期

    Args:
        token (string): Token
    """
    def tokenValid(exp):
        return int(time.time()) < exp

    token_info = getTokenInfo(token)
    return tokenValid(token_info['exp'])


def encodePasswd(passwd, pubkey):
    _key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
    _data = rsa.encrypt(passwd.encode('utf8'), _key)
    return base64.b64encode(_data).decode()


def createGqlClient(api_endpoint, token=None):
    """生成 Gql 请求

    Args:
        api_endpoint (string): 要请求的 gql url
        token (需要用的 Token, optional): 非必须 如果唯空则不添加 Token. Defaults to None.

    Returns:
        Client: 需要用到的 Gql Client
    """
    transport = RequestsHTTPTransport(url=api_endpoint, headers={
        'Authorization': token}) if token else RequestsHTTPTransport(url=api_endpoint, )
    return Client(transport=transport, fetch_schema_from_transport=True)


def execQuery(client, query, params={}, queryName=''):
    return client.execute(gql(query), variable_values=params)[queryName]
