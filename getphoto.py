import requests
import json
import os
from bs4 import BeautifulSoup
import threading


def gethtml():
    with open("F:\AI data\save_2021-0\save_2021-03-08.json",encoding="UTF-8") as load_f:
        load_dict=json.load(load_f)
        print(load_dict)
    for i in load_dict:
        html=i["qn_url"]
        print(html)
        saveImage(html)
    

'''
 下载图片
 img为获取的图片地址

'''
def saveImage(img):
    with open("F:\\AI data\\save_2021-0\\调试后图片\\"+os.path.basename(img),'wb') as f:
        f.write(requests.get(img).content)
    print(os.path.basename(img)+"保存成功")

if __name__=='__main__':
    gethtml()