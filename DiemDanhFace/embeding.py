from keras_facenet import FaceNet
from mtcnn import MTCNN
import pandas as pd 
import numpy as np 
import os
import cv2

embedder = FaceNet()
detector = MTCNN()

data = []

ID = [1,2,3]

Name = []

for file in os.listdir("person"):

    Name.append(file.split(".jpg")[0])
    path_file = os.path.join("person", file)

    img = cv2.imread(path_file)

    faces =  detector.detect_faces(img)

    face = faces[0]
    st = (face['box'][0], face['box'][1])
    en = (face['box'][0] + face['box'][2], face['box'][1] + face['box'][3])
    data.append(img[st[1] : en[1], st[0]: en[0]])

    img_show = img[st[1] : en[1], st[0]: en[0]]

    img_show = cv2.resize(img_show, (200,200))

    cv2.imshow('frame', img_show)

    cv2.waitKey(1000)

vt = embedder.embeddings(data)
print(vt.shape)

df=pd.DataFrame(data=vt, index=[i for i in range(vt.shape[0] )], columns=[str(i) for i in range( vt.shape[1] )])

df['ID'] = ID 
df['NAME'] = Name

df.to_csv("root.csv")
