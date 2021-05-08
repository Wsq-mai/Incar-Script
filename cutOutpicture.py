import cv2

name=''
svaename=''
xml_path=''
img_path=''
savePath=''

def cutOutpicture(name,area):
    path=img_path+name+'.jpg'
    img=cv2.imread(path)
    # cv2.waitKey(0) 等待键盘按下事件 0ms:长时间等待
    img=img[area[0]:area[1],area[2]:area[3]]
    savename=savePath+name+'.jpg'
    cv2.imwrite(savename,img)

def getArea(name):

    #write natation file to img path
    in_file = open(xml_path+image_id+".xml", encoding = 'utf-8')
    print(xml_path+name+".xml")
    
    # try:
    tree=ET.parse(in_file)
    root = tree.getroot()

    #size
    size=root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

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
        cutOutpicture(name,area)
    in_file.close
    return  True
