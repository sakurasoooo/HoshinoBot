import re
import os
import cv2
import time
import base64
# from . import config
import urllib.request
# import urllib
from PIL import Image, ImageDraw
from random import randint
import numpy as np
from io import BytesIO

from hoshino import util

# opencv无法使用中文路径
#PicPath = config.PIC_PATH + 'JieTou/'


async def add(purl, cascade_file=os.path.dirname(os.path.abspath(__file__))+"/data/lbpcascade_animeface.xml",qq=0):
    face_img = 0
    req = urllib.request.urlopen(purl)
    arr = np.asarray(bytearray(req.read()),dtype=np.uint8)
    cvimg = cv2.imdecode(arr,-1)
    if(qq==False):
        cascade = cv2.CascadeClassifier(cascade_file)
        # cvimg = cv2.imread(filename, cv2.IMREAD_COLOR)
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
        

        cvimg = cv2.cvtColor(cvimg,cv2.COLOR_BGR2RGB)
        face_img = Image.fromarray(cvimg)
        face_img=face_img.crop((x,y,x+w,y+h))
    else:
        cvimg = cv2.cvtColor(cvimg,cv2.COLOR_BGR2RGB)
        face_img = Image.fromarray(cvimg)
    
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

    # buf = BytesIO()
    # _img.save(buf, format='PNG')
    _img.save('./test.png')
    # base64_str = base64.b64encode(buf.getvalue()).decode()
    return util.pic2b64(_img)


async def add_head(msg):
    url = re.findall(r'http.*?term=\d', msg)[0]


    try:

        msg = await add(url)
        if (msg ):
            return msg
        else:
            return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}没找到头.png]"
    except Exception as e:
        print(repr(e))
        return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}接头失败.png]"

async def add_grouphead(msg):



    url = f'http://q1.qlogo.cn/g?b=qq&nk={msg}&s=160'


    if not os.path.exists(PicPath):
        os.makedirs(PicPath)
    try:

        msg=await add(url, qq=1)
        if (msg):
            return msg
        else:
            return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}没找到头.png]"
    except Exception as e:
        print(repr(e))
        return f"[CQ:image,file=file:///{os.path.dirname(os.path.abspath(__file__))+'/data/'}接头失败.png]"
