import re
import os
import cv2
import time
from . import config
import urllib.request
from PIL import Image, ImageDraw
from random import randint

from io import BytesIO

from hoshino import aiorequests

# opencv无法使用中文路径
#PicPath = config.PIC_PATH + 'JieTou/'


async def add(filename, outfile, cascade_file=os.path.dirname(os.path.abspath(__file__))+"/data/lbpcascade_animeface.xml",qq=0):
    img = Image.open(filename)
    face_img = img.copy()
    if(qq==False):
        cascade = cv2.CascadeClassifier(cascade_file)
        cvimg = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(24, 24))
        if not len(faces):
            return 0
        faces=list(faces)
        faces.sort(key=lambda i:int(i[2])*int(i[3]),reverse=True)
        (x, y, w, h) = faces[0]
        
        face_img=img.crop((x,y,x+w,y+h))
    fg_img = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/data/fg.png")
    bg_img = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/data/bg.png")
    id_img = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/data/id.png")
    mask_img = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/data/mask.png").convert('L')

    
    bg_img.paste(face_img.resize((600,600)), (202, 89))
    r, g, b, a = fg_img.split()
    bg_img.paste(fg_img, (0, 0),a) #fixed

    id_img.paste(face_img.resize((200,200)),(76, 464))
    _img=Image.composite(id_img, bg_img, mask_img)
    _img=_img.crop((0,68,712,687))
    _img.save(PicPath + outfile)
    return 1


async def add_head(msg):
    url = re.findall(r'http.*?term=\d', msg)[0]

    p1 = re.compile("/([^/]+)/0")

    if not os.path.exists(PicPath):
        os.makedirs(PicPath)
    try:
        file1 = p1.findall(url)[0] + ".png"

        urllib.request.urlretrieve(url, PicPath + file1)
        picname = p1.findall(url)[0] + time.strftime("%F-%H%M%S") + ".png"
        if await add(PicPath + file1, picname):
            return f"[CQ:image,file=file:///" + os.path.abspath(PicPath+picname) + "]"
        else:
            return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}没找到头.png]"
    except Exception as e:
        print(repr(e))
        return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}接头失败.png]"

async def add_grouphead(msg):

    p1 = re.compile("/([^/]+)/0")

    url = f'http://q1.qlogo.cn/g?b=qq&nk={msg}&s=160'


    if not os.path.exists(PicPath):
        os.makedirs(PicPath)
    try:
        file1 = msg + ".png"

        urllib.request.urlretrieve(url, PicPath + file1)
        picname = msg + time.strftime("%F-%H%M%S") + ".png"
        if await add(PicPath + file1, picname, qq=1):
            return f"[CQ:image,file=file:///" + os.path.abspath(PicPath+picname) + "]"
        else:
            return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}没找到头.png]"
    except Exception as e:
        print(repr(e))
        return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}接头失败.png]"
