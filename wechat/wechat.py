#coding=utf-8
from flask import Flask,request,abort,render_template
import hashlib
import xmltodict
import time
from urllib.request import urlopen
from urllib.parse import quote
import json


app = Flask(__name__)
TOKEN="wxzzliuptop"
APPID="wx557f84550c7a267b"
SECRET="fd80eb9a16ca955e1b5de06fb68d8374"
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/wechat',methods=["GET","POST"])
def wechat():
    #接受微信参数
    signature =request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    str = "signature=%s,timestamp=%s,nonce=%s"%(signature,timestamp,nonce)
    print(str)
    if not all([signature,timestamp,nonce]):
        abort("400")  #如果参数为空  返回
    li = [timestamp,nonce,TOKEN]
    li.sort()
    temp= "".join(li)
    sign = hashlib.sha1(temp.encode()).hexdigest()
    if(sign != signature):
        abort(405)
    else:
        if request.method == "GET":
            echostr = request.args.get("echostr")
            return echostr
        elif request.method == "POST":
            xmldata = request.data
            print(xmldata)
            dictdata = xmltodict.parse(xmldata)
            xmlcontent = dictdata.get("xml")
            msgtype = xmlcontent.get("MsgType")
            if msgtype == "text":
                #文本消息
                responsemsg={
                    "xml":{
                        "ToUserName":xmlcontent.get("FromUserName"),
                        "FromUserName": xmlcontent.get("ToUserName"),
                        "CreateTime":int(time.time()) ,
                        "MsgType":"text",
                        "Content":xmlcontent.get("Content")
                    }
                }
                xml_data =xmltodict.unparse(responsemsg)
                return xml_data
            else: #其他自行补充
                responsemsg = {
                    "xml": {
                        "ToUserName": xmlcontent.get("FromUserName"),
                        "FromUserName": xmlcontent.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "www.baidu.com"
                    }
                }
                xml_data = xmltodict.unparse(responsemsg)
                return xml_data

    return 'Hello World!'
@app.route("/index")
def index():
    #获取code
    code = request.args.get("code")
    print("code is %s"%code)
    #获取access_token
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"\
          %(APPID,SECRET,code)
    resp = urlopen(url)
    json_s = resp.read()
    print("json_s= %s" % json_s)
    resp_dic=json.loads(json_s)
    access_token = resp_dic.get("access_token")
    open_id = resp_dic.get("openid")
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%\
          (access_token,open_id)
    res = urlopen(url)
    json_str = res.read()
    print("json_str= %s" % json_str)
    resp_dic = json.loads(json_str)
    return render_template("index.html",user=resp_dic)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=True)  #host参数是说设置那个IP可以访问

