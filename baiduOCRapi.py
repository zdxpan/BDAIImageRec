#  使用API
#  PYthon 2 
#  根据百度AI 接口 请求，识别文字内容代码
import sys
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
import os
import urllib, urllib2, sys, json
import base64
import StringIO

#  替换下面的
APP_ID = 'x'
API_KEY = 'x'
SECRET_KEY = 'x'


url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"    # 手写文字识别
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_auth():
    apikey = API_KEY   # caojiao
    secret_key = SECRET_KEY
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (apikey, secret_key)
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        o = json.loads(content.decode())
        return o['access_token']
    return None

#---"body 请求参数   image ; language_type; detect_language;  detect_direction ;  probability ;  "---
def seturl_bodyH_get_post(url, image):
    access_token = get_auth()
    url = url +  "?access_token=%s" % access_token
    options = {}  
    options['vertexes_location'] = "true"       # 文字外接多边形顶点位置
    # options['recognize_granularity'] = 'small'
    options["language_type"] = "CHN_ENG"        # 识别语言类型：- CHN_ENG：中英文混合；...
    options["detect_direction"] = "true"        # 是否检测图像朝向，1:逆时针90度
    options["detect_language"] = "true"         # 语言检测
    options["probability"] = "true"             # 是否返回识别结果中每一行的置信度
    options['image'] = base64.b64encode(image)  # 对图片进行base64编码
    decode_data = urllib.urlencode(options)     # 将字符串进行URL编码
    
    req = urllib2.Request(url, data=decode_data)   # post请求
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header("API_KEY", API_KEY)
    res = urllib2.urlopen(req)
    content = res.read()
    if content is not None:
        rel = json.loads(content)
        return rel
    return None

# """ 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()    



img = "/Users/zhoudaoxian/Desktop/13910139906.jpg"  # 替换你图片路径

rel = seturl_bodyH_get_post(url=url, image=get_file_content(img))

for i in rel[u'words_result']:
    print(i['words'])
