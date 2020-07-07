import numpy as np #
from ngoctuhan.database import SQL_Server 
import base64
import os
import cv2
import datetime
from time import gmtime, strftime
from mtcnn import MTCNN
from keras_facenet import FaceNet

def process_bangchamcong(id_tv, thang, nam):

    query = "SELECT * FROM dbo.BangChamCong WHERE NhanVienID = {} AND MONTH(NgayLV) = MONTH('2020/{}/25') AND YEAR(NgayLV)=YEAR('{}/1/1');"

    query = query.format(id_tv,thang, nam)

    return query

def get_KhachHang(id):
    sql = SQL_Server()
    query =  "SELECT KhachHang.Id FROM dbo.KhachHang WHERE ThanVienID = " + str(id)
    data = sql.select(query)

    return data[0][0]


def get_NhanVien(id):

    sql = SQL_Server()
    query =  "SELECT * FROM ThanhVien, NhanVien WHERE ThanhVien.Id = {} AND NhanVien.ThanVienID = {} ;"
    query = query.format(id, id) 
    thanhvien = sql.select(query)
    thanhvien = np.array(thanhvien)
    # print(thanhvien[0, :])
    # NHÂN VIÊN ID NẰM VỊ TRÍ DATA[12]
    dt = datetime.datetime.today()

    year = dt.year
    month = dt.month

    query2 = process_bangchamcong(thanhvien[0, 12],month, year)

    nlv =  sql.select(query2)

    nlv =  np.array(nlv)

    # print(nlv)
    days = ['background-color:rgb(0, 80, 133);'] * 32
    # print(days)
    time_muon = 0
    songaydilam = 0
    songaymuon = 0
    for i in range(nlv.shape[0]):
        day =  nlv[i, 1].day
        muon = nlv[i, 3]

        if muon >= 15:
            days[day] = 'background-color:red;'
            time_muon += muon
            songaymuon += 1
        else:
            days[day] = 'background-color:green;'

        songaydilam += 1

    days.append(time_muon)
    days.append(songaydilam)
    days.append(songaymuon)
    
    diemdanh =  np.array(days)

    # print(days)

    res = np.concatenate((thanhvien[0,:], diemdanh), axis = 0)
    # print(res[-30:])
    return res

def random_name():
    time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    time = str(time) + '.jpg'
    return time

def have_face(res):
    imgString = res.split(',')[1]
    imgdata = base64.b64decode(imgString)
    filename = os.path.join( 'Save_ImgPost', random_name() )
    with open(filename, 'wb') as f:
        f.write(imgdata)
    img = cv2.imread( filename)
    detector = MTCNN()

    faces =  detector.detect_faces(img)

    print(faces)
    if len(faces) > 0:
        return True, filename
    else: 
        return False, filename

def extract_faceID(filename, id):
    print("BAT DAU LAY THONG TIN FACE ID")
    img = cv2.imread(filename)
    embedder = FaceNet()
    detector = MTCNN()
    data = []
    faces =  detector.detect_faces(img)
    for face in faces:
        st = (face['box'][0], face['box'][1])
        en = (face['box'][0] + face['box'][2], face['box'][1] + face['box'][3])
        data.append(img[st[1] : en[1], st[0]: en[0]])
        break
    vt = embedder.embeddings(data)[0]

    # save to database
    sql = SQL_Server()

    query =  "INSERT INTO dbo.FaceID VALUES (" + str(id) 

    for i in vt:
        query += " , " + str(i) 

    query +=  ")"

    # print(query)
    sql.insert(query)

    print("ADD FACE ID INTO CSDL THANH CÔNG")



