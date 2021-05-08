# -*- coding: utf-8 -*-
# 请先运行reanameallerro.py和renameallerro2.py
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join
from pathlib import Path
from PIL import Image
from tqdm import tqdm


# im = Image.open(filename)#返回一个Image对象
# print('宽：%d,高：%d'%(im.size[0],im.size[1]))
#存储地址
xml_path='F:/AIdata/鸟类coco/coco/'
#txt地址
txt_path='F:/AIdata/鸟类coco/coco/'
data_path=txt_path

headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""
tailstr = '''\
</annotation>
'''


classes_coco=['bird','person','cat']
#转换公式
def convert(size ,x,y,w,h):
    box=[]
    x=float(x)
    y=float(y)
    w=float(w)
    h=float(h)
    w*=size[0]
    h*=size[1]
    
    box.append(x*size[0]-(w/2)) #xmin
    box.append(y*size[1]-(h/2)) #ymin
    box.append(x*size[0]+(w/2)) #xmax
    box.append(y*size[1]+(h/2)) #ymax
    return box
#获取txt中的信息
def gettxt(txt_file,size):
    objs=[]
    print(txt_file)
    file=txt_path+txt_file
    print(file)
    with open(file,'r') as f:
            data=f.readlines()
            obj=[]
            for line in data:
                line=line.strip('\n')
                line=line.split(' ')
                print(line)
                #line[0]=classes_coco[line[0]]
                obj=convert(size,line[1],line[2],line[3],line[4])
                objs.append([classes_coco[int(line[0])],obj[0],obj[1],obj[2],obj[3]])
    print(objs)
    return objs

#地址， 头部格式 ， 对象信息 ， 尾部信息
def write_xml(anno_path, head, objs, tail):
    f = open(anno_path, "w")
    f.write(head)
    for obj in objs:
        f.write(objstr % (obj[0], int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4])))
    f.write(tail)

#获取图片size
def imagesize(image_file):
    im=Image.open(image_file)
    return im.size

fileList =os.listdir(txt_path)
for  txt_file in tqdm(fileList):
    if txt_file[-3:]=='txt':
        image_path=txt_path+txt_file[:-3]+'jpg'
        size=imagesize(image_path)
        print(size)
        head = headstr % (txt_file,size[0], size[1], 3)
        objs=gettxt(txt_file,size)
        print(objs)
        anno_path=xml_path+txt_file[:-3]+'xml'
        write_xml(anno_path,head,objs,tailstr)
