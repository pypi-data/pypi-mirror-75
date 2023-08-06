from .lib import (
    tokenExpCheck,
    encodePasswd,
    createGqlClient,
    execQuery
)
from .graphql import QUERY
PUBKEY = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
'''
HOST = 'https://core.authing.cn/graphql'


class SDKInitException(BaseException):
    pass


class Authing:
    def __init__(self, opts: dict):
        self.host = opts.get('host', HOST)
        self.pubkey = opts.get('pubkey', PUBKEY)
        self.userPoolId = opts.get('userPoolId', None)
        if not self.userPoolId:
            raise SDKInitException('userPoolId is required!')
        self.secret = opts.get('secret', None)
        self.token = opts.get('token', None)
        self.sdk = not self.token and self.userPoolId and self.secret  # 根据传进来的参数判断能否进行 SDK 的初始化
        if self.sdk:
            self.sdk_init()

    def __getattr__(self, key):
        """对于访问对象的参数进行捕获，Key 为QueryName 的名字，会根据请求的名字生成调用的 Gql 请求函数，将该函数进行返回

        Args:
            key (string): QueryName 对应要请求的 Gql 名字
        """
        def querySomeThing(params={}):
            return self.request(key, QUERY[key], params=params)
        return querySomeThing

    def get_token(self):
        """如果存在 Token 的私有变量则增加 Bearer 的头并返回
        """
        return f'Bearer {self.token}' if self.token else ''

    def get_client(self):
        """每次请求自动生成 Gql Clien，同时获取是否进行 Token 的加入
        """
        return createGqlClient(self.host, self.get_token())

    def sdk_init(self):
        """根据SDK参数进行设置 Token

        Raises:
            BaseException: Token 初始化的参数错误
        """
        res = self.getClientWhenSdkInit({
            "secret": self.secret
        })
        if "accessToken" in res:
            self.token = res['accessToken']
        else:
            raise SDKInitException(f'Token initialization failed {res}')

    def transform(self, queryName, params):
        """转换 Params 中的不标准数据 比如 registerInClient, Client, ClientId 参数，使用自带的 userpoolId 进行替换

        Args:
            queryName (string): 请求的名字
            params (string): 参数

        Returns:
            [dict]: [new params]
        """
        for user_pool_id in ['client', 'clientId', 'registerInClient']:
            if f'${user_pool_id}' in QUERY[queryName]:  # 判断是 gql 请求中是否存在要替换的元素
                params[user_pool_id] = self.userPoolId
        if 'password' in params:
            params['password'] = encodePasswd(params['password'], self.pubkey)
        if queryName == 'register':
            params['registerInClient'] = self.userPoolId
            return {'userInfo': params}
        return params

    def request(self, queryName, query, params={}):
        # 每次请求检测 Token 是否过期 如果过期则判断能否进行 SDK 初始化来刷新 Token 从而实现 Token 的 refresh
        if self.token and self.sdk and not tokenExpCheck(self.token):
            self.sdk_init()
        res = execQuery(
            self.get_client(),
            query=query,
            params=self.transform(queryName, params),
            queryName=queryName
        )
        # 判断是不是 空 Token 登录，如果是就根据 Login 以后的 Token 作为 SDK 的 Token
        if queryName in ['login'] and not self.sdk and not self.token:
            self.token = res['token']
        return res
