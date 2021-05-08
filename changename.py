import os
import re
import sys
from pypinyin import lazy_pinyin
# path=r"F:\AI data\松材线虫图片视频\2021.1月疑似枯死松树图片"

def changename(path,name):
    fileList =os.listdir(path) #待修改文件
    print("修改前："+str(fileList))
    os.chdir(path)
    xn=1
    jn=15000
    tn=1

    for filename in fileList: #遍历文件中的文件
        #py=lazy_pinyin(path)  #pinyin 返回的是list 需要转换为字符串 lazy:没有音调
        #py=''.join(py)+str(n)+'.jpg' #中间无字符

        #rint(py)
        py=""
        pat=".+(\.(jpg|jpeg|JPG|png|xml|webp|txt))" #匹配文件名（正则）
        patten=re.findall(pat,filename)  #正则匹配
        if patten[0][0]==".xml" :
            py=name+str(xn)+".xml"
            xn=xn+1
        if patten[0][0]==".jpg" or patten[0][0]==".png" or patten[0][0]==".webp":
            py=name+str(jn)+".jpg" 
            jn=jn+1 
        if patten[0][0]==".txt" :
            py=name+str(tn)+".txt"
            tn=tn+1
        os.rename(filename,(py))  #修改文件名
        print(filename,'======>',py)
        #n = n+1
    print("----------------------------------")
    sys.stdin.flush()
    print("修改后:"+str(os.listdir(path)))

if __name__=='__main__':
    # path=r"F:/AIdata/bird4/putongluzi"
    # path=r"F:/Code/python_vscode/yolo/yolov5-master/data/test"
    # path=r"F:/Code/python_vscode/yolo/coco/xml/bing"
    # path=r"F:/AIdata/鸟类/0425/漏检"
    path=r"F:/BaiduNetdiskDownload/15000~15723"
    name="val"
    flist=os.listdir(path)
    changename(path,name)
    # for fname in flist:
    #     p=path+'\\'+fname
    #     changename(p,str(fname))

