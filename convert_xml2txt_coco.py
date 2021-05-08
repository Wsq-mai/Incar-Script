# -*- coding: utf-8 -*-
# 请先运行reanameallerro.py和renameallerro2.py
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join
from pathlib import Path


classes=[ "禁止车辆","禁止非机动车","禁止超车",
        "禁止左转","禁止右转","禁止左转直行",
        "禁止右转直行","禁止左右转","禁止直行",
        "禁止驶入","禁止行人","禁止掉头",
        "禁止鸣笛","禁止骑行","禁止停车",
        "禁止长停","禁止停放",

        "限重","限速","限高","限宽",

        "停车检查","测速",

        #黄牌三角 警告注意类  
        "隧道","村庄","悬崖",
        "弯道","上坡","下坡",
        "注意行人","慢行","事故易发路段",
        "注意自行车","注意危险","注意儿童",
        "注意牲畜","注意红绿灯","注意落石",
        "注意非机动车",
        "十字交叉","T形交叉","Y形交叉",
        "环形交叉","向左急弯路","向右急弯路",
        "反向弯路","连续弯路","两侧变窄",
        "右侧变窄","左侧变窄","窄桥",
        "易滑",

        "方向信息","出口","直行中",
        "停车场","出入口信息","公交车道",
        "人行横道",

        "直行","左转","右转",
        "左右转","右转直行","左转直行",
        "直行，左转，右转","环岛","靠左侧道路",
        "靠右侧道路",

        "减速慢行","施工慢行","施工",
        "停车","步行","让"]
classes_bss=["bss"]

classes_bird=[
            "白鹭","白眼潜鸭","斑嘴鸭",
            "骨顶鸡","绿翅鸭","绿头鸭",
            "罗纹鸭","普通鸬鹚","鸳鸯",
            "红头潜鸭","牛背鹭","凤头䴙䴘",
            "小䴙䴘","彩鹬","白腰草鹬"
            ]
classes_bird1=["鸟类"]

classes_coco=['bird','person','cat', 'dog', 'horse', 'sheep', 'cow','elephant', 'bear', 'zebra', 'giraffe']

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    print(x,y,w,h)
    return (x,y,w,h)
 
def convert_annotation(image_id,xml_path,img_path):
    #'/home/incar/data/frogfire/xml/%s.xml'%(image_id)
    #write natation file to img path

    in_file = open(xml_path+image_id+".xml", encoding = 'utf-8')
    print(xml_path+image_id+".xml")
    
    # try:

    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    txt_path='F:/Code/python_vscode/data/txt/bird/'
    if size is None:
        return  False
    w = int(size.find('width').text)
    print(w)
    h = int(size.find('height').text)
    if os.path.isfile('%s/%s.txt'%(txt_path,image_id)):
        os.remove('%s/%s.txt'%(txt_path,image_id))

    out_file = open('%s/%s.txt'%(txt_path,image_id), 'a+')

    for obj in root.iter('object'):
        print(obj)
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult)==1:
        #     continue
        try:
            cls_id = classes_coco.index(cls)
        except Exception as e:
            print("Cannot read xml file {0} {1}:{2}".format(xml_path,image_id,e))

        xmlbox = obj.find('bndbox')
        if xmlbox  is None:
            continue  

        if cls_id==1:
            cls_id=2
        elif cls_id>=2:
            cls_id=1

        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        if bb[0]>1 or bb[1]>1 :
            print("cancel invalid box!{} \n".format(image_id))
            continue
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()
    
    # except Exception as e:
    #     print("Cannot read xml file {0} {1}:{2}".format(xml_path,image_id,e))
    
    in_file.close
    return  True


#将xml的数据转为同目录的txt数据，并同时生成列表文件
val_percent = 0.1#测试集占总数据集的比例，默认0.1，如果测试集和训练集已经划分开了，则修改相应代码
data_path = 'F:/Code/python_vscode/data/images/bird/'#图像在darknet文件夹的相对路径，见github的说明，根据自己需要修改，注意此处也可以用绝对路径
org_lable_path ='F:/Code/python_vscode/data/Annotations/bird/' #存放XML数据的文件夹,注意：在子目录中
# if not os.path.exists('labels/'):
#     os.makedirs('labels/')
# F:/AIdata/松材线虫/0331/漏检/  松材线虫 
# F:/Code/python_vscode/yolo/co数据集/xml co数据集
# F:/AIdata/鸟类/0406/漏检/
#F:/Code/python_vscode/yolo/coco/已标注/一批次/
#F:/AIdata/鸟类/bird/罗纹鸭/
#F:/Code/python_vscode/yolo/coco/xml/中专/

#测试
#存放XML数据的文件夹,注意：在子目录中

image_ids_items = [f for f in os.listdir(org_lable_path)]
# image_ids_child= [org_lable_path+"/"+f+"/outputs/" for f in os.listdir(org_lable_path)]
# image_ids = [s for s in image_ids_child]

train_file = open('all_coco.txt', 'w')



#org_lable_path = '/home/incar/data/bird3/纠正后标注' #存放XML数据的文件夹,注意：在子目录中

#data_path = '/home/incar/data/bird2/鸟类图片/鸟类'#图像在darknet文件夹的相对路径，见github的说明，根据自己需要修改，注意此处也可以用绝对路径


for i, image_id in enumerate(image_ids_items):
    if image_id[-3:] == "xml":
        #有些时候jpg和xml文件是放在同一文件夹下的，所以要判断一下后缀
       onlyfilename = image_id[:-3]


       file_path = data_path+"/"+image_id[:-3] + 'jpg'
       item = image_id[:-4]
       my_file = Path(file_path)
       if my_file.is_file():
          size = os.path.getsize(file_path)
          if size>0 :
            if(image_id[:-4]=="2021-3-17-12-01-02"):
                print("found file!")
            crs =  convert_annotation(item,org_lable_path,data_path)
            if crs :
                # if i < (len(image_ids) * val_percent):
                #         val_file.write(file_path+"\n") #data_path + '%s\n'%(image_id[:-3] + 'jpg')
                # else:
                train_file.write(file_path+"\n") #data_path + '%s\n'%(image_id[:-3] + 'jpg')
            else:
                print("invalidate xml file :{} \n".format(onlyfilename+".xml"))

          else:
              print("error file :%s"%(file_path))

        
train_file.close()
