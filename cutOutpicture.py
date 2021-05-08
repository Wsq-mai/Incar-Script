import cv2
import os
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join
from pathlib import Path
from PIL import Image
from tqdm import tqdm

#测试
xml_path='data/image/bailu/'
img_path='data/image/bailu/'
savePath='run/image/bailu/'

def cutOutpicture(name,area,n):
    path=img_path+name
    img=cv2.imread(path)
    # cv2.waitKey(0) 等待键盘按下事件 0ms:长时间等待
    img1=img[int(area[2]):int(area[3]),int(area[0]):int(area[1])]
    savename=savePath+name[:-4]+'_'+str(n)+'.jpg'
    print(cv2.imwrite(savename,img1))

def getArea(name):

    #write natation file to img path
    in_file = open(xml_path+name[:-4]+".xml", encoding = 'utf-8')
    print(xml_path+name+".xml")
    
    # try:
    tree=ET.parse(in_file)
    root = tree.getroot()
    #size
    size=root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    n=1
    for obj in root.iter('object'):
        print(obj)
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult)==1:
        #     continue
        xmlbox = obj.find('bndbox')
        if xmlbox  is None:
            continue  

        area=[float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]
        if area[1]-area[0]<64 or area[3]-area[2]<64:
            continue
        area=[area[0]-50,area[1]+50,area[2]-50,area[3]+50]
        if area[0]<0:
            area[0]=0
        if area[1]>w:
            area[1]=w
        if area[2]<0:
            area[2]=0
        if area[3]>h:
            area[3]=h
        cutOutpicture(name,area,n)
        n=n+1
    in_file.close
    return  True

if not savePath:
    os.makedirs(svaename)

imgList=os.listdir(img_path)
for name in tqdm(imgList):
    if name[-3:]=='jpg':
        getArea(name)
