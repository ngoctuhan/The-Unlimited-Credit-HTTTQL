import pandas as pd #
import numpy as np
from database import SQL_Server

def Norm(vt1, vt2):

    return np.sqrt(np.sum((vt1-vt2)**2))

def identification(vt):


    sql = SQL_Server()
    query = "SELECT * FROM dbo.FaceID, dbo.ThanhVien WHERE dbo.FaceID.ThanVienID = dbo.ThanhVien.Id"

    data = sql.select(query)

    data = np.array(data)
    
    ID = data[:, 514]
    # print(ID)
    X = data[:, 2:514]
    
    NAME = data[:, 515]
    
    distance = np.array([Norm(vt, i) for i in X])

    min = np.argmin(distance)

    
    if distance[min] < 0.80:

        return ID[min], NAME[min], distance[min]

    
    return None, None, None

def is_have_face(id, name):
    pass

if __name__ == "__main__":

    import cv2
    img = cv2.imread("trung.png")

    from keras_facenet import FaceNet
    embedder = FaceNet()

    vt = embedder.embeddings([img])

    id, name, distance = identification(vt[0])

    print(id, name, distance)

