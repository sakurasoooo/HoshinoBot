import re
import os
import cv2
import time
from . import config
import urllib.request
from PIL import Image, ImageDraw
from random import randint

# opencv无法使用中文路径
PicPath = config.PIC_PATH + 'JieTou/'


async def add(filename, outfile, cascade_file=os.path.dirname(os.path.abspath(__file__))+"/data/lbpcascade_animeface.xml"):
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
    img = Image.open(filename)
    img = img.convert("RGBA")
    faceimg = Image.open(os.path.dirname(os.path.abspath(__file__)) + "/data/fg.png")
    top_shift_scale = 0.45
    x_scale = 0.25
    for (x, y, w, h) in faces:
        y_shift = int(h * top_shift_scale)
        x_shift = int(w * x_scale)
        face_w = max(w + 2 * x_shift, h + y_shift)
        
       # faceimg = faceimg.resize((face_w, face_w))
        r, g, b, a = faceimg.split()
        img.paste(faceimg, (x - x_shift, y - y_shift), mask=a)
    img.save(PicPath + outfile)
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
