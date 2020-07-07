import tkinter as tk
                
from tkinter import *
import cv2
from PIL import ImageTk,Image
from datetime import date
from database import SQL_Server
from datetime import datetime


def diff_time():

    today = str(date.today()) 

    today =  today.split('-')
    y = int(today[0]) % 2000
    m =  int(today[1]) 
    d =  int(today[2])
    
    string = "{}/{}/{} 8:00:00".format(d, m, y)

    d1 = datetime.strptime(string , "%d/%m/%y %H:%M:%S")
    d2 = datetime.now()
    
    minsDiff = (d2-d1).total_seconds() / 60.0

    return int(minsDiff)

def get_notice(img, id, name, conf, time = 20):

    img = cv2.resize(img,(150,150))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    root = tk.Tk()
    root.geometry("350x350")
    id_display ="ID    : " + str(id)
    name_display = "NAME : " + str(name)
    conf_display = "CONF : " + str(conf)
    tk.Label(text=id_display, font = "Helvetica 12 bold", fg = "green",).place(x=10, y=10)
    tk.Label(text=name_display, font = "Helvetica 12 bold").place(x=10, y=40)
    tk.Label(text=conf_display, font = "Helvetica 12 bold").place(x=10, y=70)
    from datetime import datetime

    # datetime object containing current date and time
    now = datetime.now()
    now = str(now).split('.')[0]
    now =  "TIME CHECKIN : " + str(now)
    tk.Label(text=now, font = "Helvetica 12 bold").place(x=10, y=100)
    canvas = Canvas(root, width = 300, height = 250)      
    canvas.place(x=65, y=130)
    img = ImageTk.PhotoImage(im_pil)   
    canvas.create_image(20,20, anchor=NW, image=img)      

    label = tk.Label(text="Windown will close after 5s", font = "Helvetica 12 bold")
    
   
    label.place(x=10, y=310)
    label.configure(text="Windown will close after 5s")   

    root.after(3000, lambda: root.destroy())
    mainloop() 

    print("LƯU VÀO CSDL")
    sql = SQL_Server()
    today = date.today()
    query = "SELECT Id FROM dbo.NhanVien WHERE ThanVienID = {}".format(id)
    data = sql.select(query)
    # dd/mm/YY
    d1 = today.strftime("%m/%d/%Y")
    id_nv = data[0][0]

    query2 = "INSERT INTO dbo.BangChamCong VALUES('{}', '{}', {}, {})".format(str(d1), str(now),diff_time(), id_nv )
    # data = sql.select(query)
    
    sql.insert(query2)
    print("ĐÃ ĐIỂM DANH THÀNH CÔNG")
    # save in database

if __name__ == "__main__":
    # get_notice(cv2.imread("face.jpg"), "1", "HOANG MAU TRUNG", "0.89")
    # sql = SQL_Server()
    query = "SELECT Id FROM dbo.NhanVien WHERE ThanVienID = {}".format(1)

    # data = sql.select(query)
    # print(data[0][0])

    # from datetime import date

    # today = date.today()
    # print(str(today))
    # # dd/mm/YY
    # d1 = today.strftime("%d/%m/%Y")
    # print("d1 =", d1)
    # d2 = datetime.now()
    # d1 = datetime.strptime("5/7/20 8:00", "%d/%m/%y %H:%M")

    # daysDiff = (d2-d1).total_seconds() / 60.0
    # print (daysDiff)

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print(now)

    # print(diff_time())
    
    

