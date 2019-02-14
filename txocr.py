# coding: utf-8

# import sys
# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde

import hashlib  
import time  
import random  
import string
import requests  
import base64  
import requests
import cv2
import numpy as np
from urllib import urlencode
import json 

# caojiao
appid = "2111930335"
appkey = "ye1i7bjYBrCcB4Jb"

#  mengyao
appid = "2111931001"
appkey = "MSHOgpyd5ycBC5Nz"

# zdx
appid = '2111435318'
appkey = 'izx4fOqgtab2BGq1'

sappid = ["2111930335", "2111931001", '2111435318']
sappkey = ["ye1i7bjYBrCcB4Jb", "MSHOgpyd5ycBC5Nz", 'izx4fOqgtab2BGq1']
url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr'  

def set_appkey(index=0):
    appid = sappid[index]
    appkey = sappkey[index]
    url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr'  

# url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr'  
# url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'  

def get_params(appid,appkey,img):
    time_stamp=str(int(time.time())) 
    nonce_str = ''.join(str(random.choice(range(10))) for _ in range(10))
    params = {'app_id':appid,                 # 请求包，需要根据不同的任务修改，基本相同
              'image':img,                    # 文字类的任务可能是‘text’，由主函数传递进来
              'time_stamp':time_stamp,        # 时间戳，都一样
              'nonce_str':nonce_str,          # 随机字符串，都一样
             }
    sort_dict= sorted(params.items(), key=lambda item:item[0], reverse = False)  #字典排序
    sort_dict.append(('app_key',appkey))   #尾部添加appkey
    rawtext= urlencode(sort_dict).encode()  #urlencod编码
    sha = hashlib.md5()    
    sha.update(rawtext)
    md5text= sha.hexdigest().upper()        # MD5加密计算
    params['sign']=md5text                  # 将签名赋值到sign
    return  params                          # 返回请求包

# 用opencv读入图片
def txocr(img):
	# frame=cv2.imread(path)
    # appid, appkey = appid, appkey
    frame = img
    nparry_encode = cv2.imencode('.jpg', frame)[1]
    data_encode = np.array(nparry_encode)
    img = base64.b64encode(data_encode)    # 得到API可以识别的字符串
    params = get_params(appid, appkey, img)    # 获取鉴权签名并获取请求参数
    res = requests.post(url,params).json()
    if res:
        return res
    return None

