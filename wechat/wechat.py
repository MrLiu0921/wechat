#coding=utf-8
from flask import Flask,request,abort
import hashlib
import xmltodict
import time

app = Flask(__name__)
TOKEN="wxzzliuptop"

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
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=True)  #host参数是说设置那个IP可以访问