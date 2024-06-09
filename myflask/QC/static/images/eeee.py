from flask import Flask, render_template, request, send_file, Response
import os
import cv2
from io import BytesIO
import base64
import json


filepath = 'myflask\QC\static\images\SN20240530000.jpg'


def encode_image(img):
    # OpenCV 이미지를 base64로 인코딩
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode('utf-8')
    # print(img_str)
    return img_str

img = cv2.imread(filepath)

img_str = encode_image(img)

print(img_str)