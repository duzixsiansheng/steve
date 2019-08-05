import os
import xml.dom.minidom
import cv2 as cv
from PIL import Image

ImgPath = 'test/'
AnnoPath = 'testxml/'
types = ['lsqxz', 'xcxjlybz', 'lslmqk', 'lsqbm', 'lsqdp', 'lsqlm', 'wtxztc' , 'xcxjlybz', 'xcxjqlm', 'xjjqls', 'xjjsd', 'xztc']
imagelist = os.listdir(ImgPath)
a = 0
for image in imagelist:

    image_pre, ext = os.path.splitext(image)
    imgfile = ImgPath + image
    xmlfile = AnnoPath + image_pre + '.xml'

    # 打开xml文档
    DOMTree = xml.dom.minidom.parse(xmlfile)
    # 得到文档元素对象
    collection = DOMTree.documentElement
    # 读取图片
    #img = cv.imread(imgfile)
    img = Image.open(imgfile)

    filenamelist = collection.getElementsByTagName("filename")
    filename = filenamelist[0].childNodes[0].data
    print(filename)
    # 得到标签名为object的信息
    objectlist = collection.getElementsByTagName("object")

    for objects in objectlist:
        # 每个object中得到子标签名为name的信息
        namelist = objects.getElementsByTagName('name')
        # 通过此语句得到具体的某个name的值
        objectname = namelist[0].childNodes[0].data

        bndbox = objects.getElementsByTagName('bndbox')
        print(objectname)
        for box in bndbox:
            print(a)
            x1_list = box.getElementsByTagName('xmin')
            x1 = int(x1_list[0].childNodes[0].data)
            y1_list = box.getElementsByTagName('ymin')
            y1 = int(y1_list[0].childNodes[0].data)
            x2_list = box.getElementsByTagName('xmax')
            x2 = int(x2_list[0].childNodes[0].data)
            y2_list = box.getElementsByTagName('ymax')
            y2 = int(y2_list[0].childNodes[0].data)
            #cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
            #cv.putText(img, objectname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
            #           thickness=2)
            print(x1,y1,x2,y2)
            region = img.crop((x1, y1, x2, y2))
            #if objectname is 'lsqxz':
            region.save(os.path.join(objectname + '/', str(a) + objectname + ".png"))
            #else:
                #region.save(objectname + ".png")
            a += 1

            #cv.imshow('head', img)
            #cv.imwrite("test/havatry.jpg", img)
