import random
import string
import base64
import pytest
from .authing import Authing, SDKInitException
from .lib import (
    getTokenInfo,
    encodePasswd,
    createGqlClient,
    execQuery
)
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoieGlleWFuZ0Bkb2RvcmEuY24iLCJpZCI6IjVlNzQ3M2VkYWQxZWJhMjMzNzgxZjZkZCIsImNsaWVudElkIjoiNTlmODZiNDgzMmViMjgwNzFiZGQ5MjE0In0sImlhdCI6MTU4NDY5NzY3OSwiZXhwIjoxNTg1OTkzNjc5fQ.RnJRnAcbWFfEWl152nd23Xh7DPH-_Hk9LLbiHyzjSbE'
PUBKEY = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
'''
API_ENDPOINT = 'https://core.authing.cn/graphql'
TEST_USERNAME = 'test'
TEST_PASSWORD = '123123'
QUERY = '''query {
            QueryOIDCAppInfoByDomain (domain: "sign") {   
              _id
              name
              domain
              image
              clientId
              css
              confirmAuthorization
              customStyles {
                forceLogin
                hideQRCode
                hideUP
                hideUsername
                hideRegister
                hidePhone
                hideSocial
                hideClose
                defaultLoginMethod
                hidePhonePassword
                placeholder {
                  username
                  email
                  password
                  confirmPassword
                  verfiyCode
                  newPassword
                  phone
                  phoneCode
                }
                qrcodeScanning {
                  interval
                  tips
                }
              }
            }
          }
'''
userPoolId = '5f0c2597061ec4de51237379'
secret = 'df9f6828b0960671a34287f2381dfb8a'


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters).lower() for i in range(length))
    return result_str


def test_getTokenInfo():
    assert getTokenInfo(TOKEN) == {
        "data": {
            "email": "xieyang@dodora.cn",
            "id": "5e7473edad1eba233781f6dd",
            "clientId": "59f86b4832eb28071bdd9214"
        },
        "iat": 1584697679,
        "exp": 1585993679
    }


def test_tokenExpCheck():
    pass


def test_encodePasswd():
    password = str(random.randint(10000, 99999))
    assert password


def test_createGqlClient():
    client = createGqlClient(API_ENDPOINT)
    assert client


def test_query():
    client = createGqlClient(API_ENDPOINT)
    result = execQuery(client, query=QUERY, params={
    }, queryName='QueryOIDCAppInfoByDomain')
    assert result['_id'] == '5e3ce9dadf5382920a69a76a'


def test_SDKInit():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    assert auth.token


def test_SDKInit_fail():
    with pytest.raises(BaseException):
        assert Authing({
            "userPoolId": userPoolId,
            "secret": '1111',
        })


def test_TokenRequest():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.checkLoginStatus({
        "token": auth.token
    })
    assert res


def test_login():
    auth = Authing({"userPoolId": userPoolId, })
    auth.login({
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })
    assert auth.token


def test_register():
    username = get_random_string(10)
    password = get_random_string(10)
    auth = Authing({"userPoolId": userPoolId, "secret": secret})
    res = auth.register({
        "username": username,
        "password": password
    })
    assert res['username'] == username


def test_users():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.users()
    assert res
