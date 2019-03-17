import hashlib

"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx557f84550c7a267b&redirect_uri=http%3A//py.aiyue0429.top/index&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"

url = "http://py.aiyue0429.top/index"

from urllib.parse import quote

print(quote(url))