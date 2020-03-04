#coding:utf-8

from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import os
int_dir = "/Users/zhoudaoxian/Desktop/intern_test/intern/"


xmls = []
for root,dirs,files in os.walk(int_dir):
    for file in files:
#         print(dirs)
        fi = os.path.join(root,file)
        if fi.endswith("xml"):
            xmls.append(fi)
x = xmls[0]            


def parse_xml(x):
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(x)
    collection = DOMTree.documentElement

    # 在集合中获取所有filename width，depth，
    info = {}
    filename = collection.getElementsByTagName("filename")[0].childNodes[0].data
    # size 
    width = collection.getElementsByTagName("size")[0].getElementsByTagName('width')[0].childNodes[0].data
    height = collection.getElementsByTagName("size")[0].getElementsByTagName('height')[0].childNodes[0].data
    depth =  collection.getElementsByTagName("size")[0].getElementsByTagName('depth')[0].childNodes[0].data
    info["name"] = filename
    info["width"] = width
    info["depth"] = depth

    # object 处理
    anotations = []
    anotation = {}
    objs = collection.getElementsByTagName("object")
    for obj in objs:
        dif = obj.getElementsByTagName("difficult")[0].childNodes[0].data
        nm =  obj.getElementsByTagName("name")[0].childNodes[0].data
        bdbox =  obj.getElementsByTagName("bndbox")[0]
        x = bdbox.getElementsByTagName('xmin')[0].childNodes[0].data
        y = bdbox.getElementsByTagName("ymin")[0].childNodes[0].data
        w = bdbox.getElementsByTagName("xmax")[0].childNodes[0].data
        h = bdbox.getElementsByTagName("ymax")[0].childNodes[0].data
        anotation["diffcult"] = dif
        anotation["coordinate"] = {"x":x,"y":y}
        anotation["width"] = w
        anotation["height"] = h
        anotation["type"] = nm
        anotations.append(anotation)
    
    rel = "{},{}".format(info,anotations)
    return rel






xmls = []
result = []
err = []
for root,dirs,files in os.walk(int_dir):
    for file in files:
        fi = os.path.join(root,file)
        if fi.endswith("xml"):
            xmls.append(fi)
            try:
                rel = parse_xml(fi)
                result.append(rel)
            except :
                err.append(fi)
                continue
with open("./result.csv" , "w") as f:
    for i in result:
        f.write("{}\n".format(i))


