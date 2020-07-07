from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import Flask
from ngoctuhan.database import SQL_Server
from ngoctuhan.utils import get_NhanVien, get_KhachHang
from ngoctuhan.utils import have_face
import threading
from ngoctuhan.utils import extract_faceID
from ngoctuhan.util import Handel
from ngoctuhan.sendSMS import send_sms


app = Flask(__name__)

@app.route('/')
@app.route('/login')
def hello():
    return render_template("index.html")

@app.route('/create_employe/<id>')
def create_employe(id):
   return render_template("create_employe.html")


@app.route('/update_infor/<id>')
def update_infor(id):
    return render_template("update_infor.html")

@app.route('/customer/<id>')
def customer(id):
    return render_template("homekh.html", id =  id)


@app.route('/save_infor', methods = ['POST'])
def save_infor():
    if request.method == 'POST':

        data = request.get_json()
        
        # save csdl 

        filename = None
        if ("avt" not in data.keys()) :
            # update in csdl 
            res= {}
            res['status'] = 'Vui lòng tải ảnh avatar'

            return jsonify(res)
        elif ("cmtnd1" not in data.keys()) or ("cmtnd2" not in data.keys()):
            res= {}
            res['status'] = 'Vui lòng upload ảnh chứng minh thư nhân dân'

            return jsonify(res)
        elif "avt" in data.keys():

            check, filename =  have_face(data["avt"])
            # print(check, filename)
            if check == False:
                res = {}
                res['status'] = 'Upload ảnh có khuôn mặt để sử dụng chức năng điểm danh'

                return jsonify(res)
            else:
                print("Lưu vào CSDL")
                # save thông in vào cớ ở dữ liệu
                query_update = "UPDATE dbo.ThanhVien SET CMND = '" + data['cmtnd'] + "', DiaChi = N'" + data['diachi']+ "', Tinh = N'" + data['tinh'] + "', Activate = 1 WHERE Id = " + data['id'] + ";"; 
                
                sql = SQL_Server()
                sql.insert(query_update)

                del sql #

                sql = SQL_Server() #
                query_insert =  "INSERT INTO dbo.NhanVien VALUES(N'{}', N'{}', {}, {}, {}, '{}', '{}', '{}', {});"
                query_insert = query_insert.format(data['vitri'], "Nhân viên", 100, 0, 1.2, data['avt'], data['cmtnd1'], data['cmtnd2'], data['id'])

                # print(query_insert)
                sql.insert(query_insert)

                t1 = threading.Thread(target=extract_faceID, args=(filename,data['id']))
                t1.start()

                res = {}
                res['status'] = 'Cập nhật thông tin thành công'


                return jsonify(res)


@app.route('/admin-page/<adminid>')
def admin(adminid):

    # get avata of admin 
    sql = SQL_Server()
    quanly = get_NhanVien(adminid)
    
    return render_template('admin_page.html', data = quanly)

@app.route('/checklogin', methods=['POST'])
def checklogin():
    if request.method == 'POST':

        data = request.get_json()
        username = data['username']
        password = data['password']


        print(data)
        sql = SQL_Server()
        query = "SELECT * FROM dbo.ThanhVien WHERE Username = '" + username + "'and Password = '" + password + "';"
        cusor = sql.select(query)
        if len(cusor) == 0:
            data = {}
            data['status'] = "Thông tin tài khoản/mật khẩu không chính xác."
            return jsonify(data)
        else:
            # check role 0: nhân viên, 1: khách hàng
            for row in cusor:
                status = row[-1]
                if status == 2: # đăng nhập lần đầu , còn bước chuyển trang web nữa.
                    data = {}
                    data['status'] = 'success'
                    data['redirect'] = 'http://192.168.16.100:5000/update_infor/' + str(row[0])
                    return jsonify(data)
                else:
                    # đăng nhập từ lần t2 trở đi
                    role = row[-2]
                    if int(role) == 2:
                        data = {}
                        data['status'] = 'success'
                        data['redirect'] = 'http://192.168.16.100:5000/admin-page/' + str(row[0])
                        return jsonify(data)
                    elif int(role) == 0:  # đã hoàn thành xong nhé.
                        # là nhân viên 
                        data = {}
                        data['status'] = 'success'
                        data['redirect'] = 'http://192.168.16.100:5000/staff/' + str(row[0])
                        return jsonify(data)
                    else:
                        # là khách hàng thì phải xử lý thêm đi chứ.
                        data = {}
                        data['status'] = 'success'
                        data['redirect'] = 'http://192.168.16.100:5000/customer/' + str(row[0])
                        return jsonify(data)
                break
@app.route('/staff/<personID>')
def personal(personID):

    nhanvien = get_NhanVien(personID)
    return render_template("staff_home.html", data =  nhanvien)

@app.route('/dataAccount', methods = ['POST'])
def dataAccount():
    if request.method == 'POST':
        data = request.get_json()

        sql = SQL_Server()
        query = "SELECT * FROM db_Credit_TheUnlimited.dbo.ThanhVien WHERE (Email = '" +  data['email'] + "' OR Sdt = '" + data['sdt'] + "' OR Username = '" + data['username'] + "')"
        tmp = sql.select(query)
        res = {}  
        if len(list(tmp)) > 0:
            
            res['status'] = "Email hoặc số điện thoại hoặc tài khoản đã tồn tài trong CSDL"
            
        else:
            res['status'] = 'Tạo tài khoản: ' + data['username'] + " thành công"

            query = "INSERT INTO db_Credit_TheUnlimited.dbo.ThanhVien VALUES ( N'" + data['hoten']+"', ' ' ,' ', ' ', '"+data['username']+"', '"+data['password']+"', '', '"+data['email']+"', '"+data['sdt']+"', '0', '2')"
            sql.insert(query)

        return jsonify(res)
    
    else:
        return "Không hỗ trợ phương thức GET"


###############----------------------------LANH ANH----------------------------------------------------------------

@app.route('/taohopdong/<id>')
def taohopdong(id):
    
    sql = SQL_Server()
    query = "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, dbo.HopDongTraGop.Giatri, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt FROM dbo.ThanhVien, dbo.HopDongTraGop, dbo.KhachHang "
    query+=" WHERE dbo.HopDongTraGop.Activate = 1 "
    query+=" AND dbo.HopDongTraGop.KhacHangID = dbo.KhachHang.Id "
    query+=" AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id "
    tmp = sql.select(query)
    tmp_data = []
    i = 1
    for row in tmp:
        tmp_data.append([i, row[0], row[1], row[2], row[4], row[3]])
        i=i+1
    del sql

    return render_template("taohopdong.html" , data = tmp_data)

@app.route('/datahoso', methods = ['POST'])
def datahoso():

    sql = SQL_Server()
    data = request.form['hopdong']
    ress = {}
    query = "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, dbo.HopDongTraGop.Giatri, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt FROM dbo.ThanhVien, dbo.HopDongTraGop, dbo.KhachHang "
    query+=" WHERE dbo.HopDongTraGop.Activate = 1 "
    query+=" AND dbo.HopDongTraGop.KhacHangID = dbo.KhachHang.Id "
    query+=" AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id AND dbo.ThanhVien.CMND = " +str(data)
    print(query)
    res = sql.select(query)
    del sql
    if len(res) == 0:
        ress['status'] = "no"
    else:
        ress['status'] = "yes"
    tmp_res = {}
    tmp_data = []
    ii = 1
    for row in res:
        tmp_data.append([ii, row[0], row[1], row[2], row[4], row[3]])
        ii=ii+1
    i = 0
    for row in tmp_data:
        tmp_res[str(i)] = [str(i) for i in row]
        i=i+1
    ress['data'] = tmp_res

    return jsonify(ress)

@app.route('/datahosothem', methods = ['POST'])
def datahosothem():
    data = request.get_json()
    # print(data)
    sql = SQL_Server()
    query1 = "SELECT dbo.KhachHang.Id FROM dbo.ThanhVien, dbo.KhachHang "
    query1+=" WHERE dbo.ThanhVien.Id =  dbo.KhachHang.ThanVienID "
    query1+=" AND dbo.ThanhVien.CMND ='" +str(data['cmnd'])+"'"
    # print(query1)
    data_id_kh = sql.select(query1)
    del sql
    sql = SQL_Server()
    query1 = "SELECT dbo.PhongGiaoDich.Id FROM dbo.ThanhVien, dbo.PhongGiaoDich "
    query1+=" WHERE dbo.ThanhVien.Tinh =  dbo.PhongGiaoDich.Tinh "
    query1+=" AND dbo.ThanhVien.Id = " +str(data['id'])
    data_id_pgd = sql.select(query1)
    # print(data['giatri'])/
    # print(data['thoihan'])
    stmoithang = float(data['giatri'])
    thoihan = float(data['thoihan'])
    tmp = stmoithang*0.015
    stmoithang+=tmp-float(data['tratruoc'])
    stmoithang=stmoithang/thoihan
    query_insertTv = "INSERT INTO dbo.HopDongTraGop (NgayMoHD, TenSP, Giatri, ThoiHan, Tratruoc, Moithang, Laisuat, KhacHangID, PGDId, Activate) VALUES ('{}', N'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    query_insertTv1 = query_insertTv.format(data['nmhd'], data['tsp'], data['giatri'], data['thoihan'], data['tratruoc'], stmoithang, 0.15, data_id_kh[0][0], data_id_pgd[0][0], 1)
    sql.insert(query_insertTv1)
    ress = {}
    del sql
    sql = SQL_Server()
    query = "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, dbo.HopDongTraGop.Giatri, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt FROM dbo.ThanhVien, dbo.HopDongTraGop, dbo.KhachHang "
    query+=" WHERE dbo.HopDongTraGop.Activate = 1 "
    query+=" AND dbo.HopDongTraGop.KhacHangID = dbo.KhachHang.Id "
    query+=" AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id"
    res = sql.select(query)
    del sql
    if len(res) == 0:
        ress['status'] = "no"
    else:
        ress['status'] = "yes"
    tmp_res = {}
    tmp_data = []
    ii = 1
    for row in res:
        tmp_data.append([ii, row[0], row[1], row[2], row[4], row[3]])
        ii=ii+1
    i = 0
    for row in tmp_data:
        tmp_res[str(i)] = [str(i) for i in row]
        i=i+1
    ress['data'] = tmp_res
    return jsonify(ress)

@app.route('/thongke/<id>')
def thongke(id):
    sql = SQL_Server()
    query = "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, HDTG.Giatri, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt "
    query += "FROM dbo.ThanhVien, dbo.KhachHang, "
    query +="(SELECT dbo.HopDongTraGop.Giatri, dbo.HopDongTraGop.Activate, dbo.HopDongTraGop.KhacHangID FROM dbo.HopDongTraGop, dbo.ThanhVien, dbo.PhongGiaoDich "
    query +="WHERE dbo.HopDongTraGop.PGDId = dbo.PhongGiaoDich.Id "
    query += "AND dbo.PhongGiaoDich.Tinh = dbo.ThanhVien.Tinh "
    query += "AND dbo.ThanhVien.Id =" + str(id) +" ) AS HDTG"
    query +=" WHERE HDTG.Activate = 1"
    query +=" AND HDTG.KhacHangID = dbo.KhachHang.Id"
    query += " AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id "
    tmp = sql.select(query)
    tmp_data = []
    i = 1
    tien = 0
    for row in tmp:
        tmp_data.append([i, row[0], row[1], row[3], row[4], row[2]])
        tien+=int(row[2])
        i=i+1
    del sql
    sql = SQL_Server()
    query += "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, HDTTD.HanmucChiTieu, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt "
    query += " FROM dbo.ThanhVien, dbo.KhachHang," 
    query += " (SELECT dbo.HopDongMoTheTD.HanmucChiTieu, dbo.HopDongMoTheTD.Activate, dbo.HopDongMoTheTD.KhacHangID FROM dbo.HopDongMoTheTD, dbo.ThanhVien, dbo.PhongGiaoDich "
    query += " WHERE dbo.HopDongMoTheTD.PGDId = dbo.PhongGiaoDich.Id "
    query += " AND dbo.PhongGiaoDich.Tinh = dbo.ThanhVien.Tinh "
    query += " AND dbo.ThanhVien.Id =" + str(id) +" ) AS HDTTD "
    query += " WHERE HDTTD.Activate = 1 "
    query += " AND HDTTD.KhacHangID = dbo.KhachHang.Id"
    query += " AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id"
 
    tmp = sql.select(query)
    for row in tmp:
        tmp_data.append([i, row[0], row[1], row[3], row[4], row[2]])
        tien+=int(row[2])
        i=i+1
    tmp_data.append([" ", " ", " ", " ", "Tổng: ", tien])
    return render_template("thongke.html" , data = tmp_data)
@app.route('/datathongke', methods = ['POST'])
def datathongke():

    sql = SQL_Server()
    data = request.form['hopdong']
    dataa = data.split()
    data = dataa[1]
    ress = {}
    query = "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, HDTG.Giatri, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt "
    query += " FROM dbo.ThanhVien, dbo.KhachHang, "
    query +=" (SELECT dbo.HopDongTraGop.Giatri, dbo.HopDongTraGop.Activate, dbo.HopDongTraGop.KhacHangID, dbo.HopDongTraGop.NgayMoHD FROM dbo.HopDongTraGop, dbo.ThanhVien, dbo.PhongGiaoDich "
    query +=" WHERE dbo.HopDongTraGop.PGDId = dbo.PhongGiaoDich.Id "
    query += " AND dbo.PhongGiaoDich.Tinh = dbo.ThanhVien.Tinh "
    query += " AND dbo.ThanhVien.Id =" + str(dataa[-1]) +" ) AS HDTG"
    query +=" WHERE HDTG.Activate = 1"
    query +=" AND HDTG.KhacHangID = dbo.KhachHang.Id"
    query += " AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id "
    query+=" AND MONTH(HDTG.NgayMoHD) = MONTH('2017/" +str(data)+ "/25');"
    res = sql.select(query)
    del sql
    tmp_res = {}
    tmp_data = []
    ii = 1
    tien = 0
    for row in res:
        tmp_data.append([ii, row[0], row[1], row[3], row[4], row[2]])
        tien+=int(row[2])
        ii=ii+1
    sql = SQL_Server()
    query += "SELECT dbo.ThanhVien.HoTen, dbo.ThanhVien.CMND, HDTTD.HanmucChiTieu, dbo.ThanhVien.Email, dbo.ThanhVien.Sdt "
    query += " FROM dbo.ThanhVien, dbo.KhachHang," 
    query += " (SELECT dbo.HopDongMoTheTD.HanmucChiTieu, dbo.HopDongMoTheTD.Activate, dbo.HopDongMoTheTD.KhacHangID,dbo.HopDongMoTheTD.NgayMoThe FROM dbo.HopDongMoTheTD, dbo.ThanhVien, dbo.PhongGiaoDich "
    query += " WHERE dbo.HopDongMoTheTD.PGDId = dbo.PhongGiaoDich.Id "
    query += " AND dbo.PhongGiaoDich.Tinh = dbo.ThanhVien.Tinh "
    query += " AND dbo.ThanhVien.Id =" + str(dataa[-1]) +" ) AS HDTTD"
    query += " WHERE HDTTD.Activate = 1 "
    query += " AND HDTTD.KhacHangID = dbo.KhachHang.Id"
    query += " AND dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id"
    query+=" AND MONTH(HDTTD.NgayMoThe) = MONTH('2017/" +str(data)+ "/25');"
    res = sql.select(query)
    for row in res:
        tmp_data.append([ii, row[0], row[1], row[3], row[4], row[2]])
        tien+=int(row[2])
        ii=ii+1
    tmp_data.append([" ", " ", " ", " ", "Tổng: ", tien])
    i = 0
    for row in tmp_data:
        tmp_res[str(i)] = [str(i) for i in row]
        i=i+1
  
    ress['data'] = tmp_res
 
    return jsonify(ress)


####------------------------------------------------VIỆT-----------------------------------------------------


@app.route('/taohoso/<id>')
def taoHoSo(id):
    return render_template("TaoHoso.html")


@app.route('/thanhtoan/<id>')
def thanhtoan(id):
    return render_template("ThanhToan.html")


@app.route('/lotrinhthanhtoan/<id>')
def lotrinhthanhtoan(id):
    return render_template("LoTrinhThanhToan.html")


@app.route('/dataHoSo', methods=['POST'])
def predict():
    if request.method == 'POST':
        res = {}
        data = request.get_json()
      
        sql = SQL_Server()
        handel = Handel()
        ten = handel.handel_Hoten(data["hoten"])

        query_check_email = "SELECT * FROM dbo.ThanhVien WHERE Email = '{}' OR CMND = '{}' OR Sdt = '{}'"
        query_check_email = query_check_email.format(data['email'], data['cmt'], data['sdt'])
        if (len(list(sql.select(query_check_email))) > 0):
            res['check_email'] = "Email/CMDN/Số điện thoại đã được sử dụng"
            return jsonify(res)
        else:
            username = handel.get_username(ten)
            password = handel.get_password()
            query_insertTv = "INSERT INTO dbo.ThanhVien (HoTen, CMND, DiaChi, Tinh, Username, Password, Nsinh, Email, Sdt, Loai, Activate) VALUES (N'{}', '{}', N'{}', '{}', N'{}', '{}', '{}', '{}', '{}', '{}', '{}')"
            query_insertTv1 = query_insertTv.format(data["hoten"], data["cmt"], data["dia_chi"], data["tinh"],username, password, data["ngaysinh"], data["email"], data["sdt"], 1, 1)
            # print(query_insertTv1)

            
            sql.insert(query_insertTv1)

            cursor = sql.select(query_check_email)
            for i in cursor:
                idTv = i[0]
            
            sdt = str(data["sdt"])
            sdt = sdt[1:]
            sdt = "+84" + sdt
            print(sdt)
            mess = 'Your Account The Unlimted \n username: {} \n password: {}'
            mess =  mess.format(username, password)
            t1 = threading.Thread(target=send_sms, args=(sdt, mess))
            t1.start()

            res['id_tv'] = idTv
            res['username'] = username
            res['password']= password

            return jsonify(res)


@app.route('/dataKhachHang', methods=['POST'])
def khachHang():
    if request.method == 'POST':
        data = request.get_json()

        sql = SQL_Server()
        insert_kh = "INSERT INTO dbo.KhachHang(Chungthuctaisan, Diem, ThanVienID) VALUES('{}', '{}', '{}')"
        insert_khFn = insert_kh.format(data["luong"], 100, data["id_tv"])
      
        sql.insert(insert_khFn)
      
    res = {}
    res['status'] = "Đã tạo tài khoản khách hàng thành công!"
    return jsonify(res)


@app.route('/dataHopDong/<id>', methods=['GET'])
def dataHopDong(id): # đã sửa xong

    tmp_data_TG = []
    tmp_data_TTD = []
    data_hopdong = {}

    id_kh = get_KhachHang(id)
    print(id_kh)
    sql = SQL_Server()
   
    print("Mã Khách hàng",id_kh)

    queryTG = "SELECT * FROM dbo.HopDongTraGop WHERE KhacHangID = {} AND Activate = 1"
    queryTG = queryTG.format(id_kh)
    cursorTG = list(sql.select(queryTG))

    for row in cursorTG:
        tmp_data_TG.append([row[0], row[1], row[2], row[3], row[4],
                            row[5], row[6], row[7], row[8], row[9], row[10]])

    queryTTD = "SELECT * FROM dbo.HopDongMoTheTD WHERE KhacHangID ={} AND Activate = 1"

    queryTTD = queryTTD.format(id_kh)
    cursorTTD = list(sql.select(queryTTD))
    for row in cursorTTD:
        tmp_data_TTD.append([row[0], row[1], row[2], row[3],
                             row[4], row[5], row[6], row[7], row[8], row[9]])

    for i in range(len(tmp_data_TTD)):
        tmp_data_TTD[i][1] = str(tmp_data_TTD[i][1])

    for i in range(len(tmp_data_TG)):
        tmp_data_TG[i][1] = str(tmp_data_TG[i][1])


    # if len(tmp_data_TTD) > 0:
    #     data_hopdong['status1'] = 'True'
    # else:
    #     data_hopdong['status1'] = 'False'

    # if len(tmp_data_TG) > 0:
    #     data_hopdong['status2'] = 'True'
    # else:
    #     data_hopdong['status2'] = 'False'


    data_hopdong["HopDongTTD"] = tmp_data_TTD
    data_hopdong["HopDongTG"] = tmp_data_TG

    print(tmp_data_TTD)
    print(tmp_data_TG)
    return jsonify(data_hopdong)


@app.route('/dataThanhToan/<id>', methods=['POST'])
def dataThanhtoan(id): # đã sửa xong

    dataHopDong = request.get_json()

    sql = SQL_Server()

    tmp_data_TDTG = []
    tmp_data_TDTTD = []
    data_thanhtoan = {}

    id_kh = get_KhachHang(id)
    # print("KHÁCH HÀNG: ", id_kh)

    if (len(dataHopDong["HopDongTTD"]) != 0):
        queryTTD = "SELECT * FROM dbo.ThanhToanTheTD WHERE KhacHangID = {} AND HDTTDID = '{}'"
        queryTTD_Fomart = queryTTD.format(id_kh, dataHopDong["HopDongTTD"][0][0])

        cursorTTD = list(sql.select(queryTTD_Fomart))
        for row in cursorTTD:
            tmp_data_TDTTD.append(
                [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    if (len(dataHopDong["HopDongTG"]) != 0):
        queryTG = "SELECT * FROM dbo.ThanhToanHDTG WHERE KhacHangID ='1' AND HDTGId = '{}'"
        queryTG_Fomart = queryTG.format(dataHopDong["HopDongTG"][0][0])

        cursorTG = list(sql.select(queryTG_Fomart))
        for row in cursorTG:
            tmp_data_TDTG.append(
                [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    for i in range(len(tmp_data_TDTTD)):
        tmp_data_TDTTD[i][1] = str(tmp_data_TDTTD[i][1])

    for i in range(len(tmp_data_TDTG)):
        tmp_data_TDTG[i][1] = str(tmp_data_TDTG[i][1])

    data_thanhtoan["ThanhToanTTD"] = tmp_data_TDTTD
    data_thanhtoan["ThanhToanTG"] = tmp_data_TDTG

    return jsonify(data_thanhtoan)


@app.route('/addthanhtoanTG', methods=['POST'])
def addthanhtoanTG():
    # print("da vao add thanh toan")
    dataAddthanhtoanTG = request.get_json()
    sql = SQL_Server()

    insert_ttTG = "INSERT INTO dbo.ThanhToanHDTG(NgayTT, Thang, Sotien, Noidung, KhacHangID, HDTGId) VALUES('{}', '{}', '{}', N'{}', '{}', '{}')"
    insert_ttTGFn = insert_ttTG.format(dataAddthanhtoanTG["date"], dataAddthanhtoanTG["thang"], dataAddthanhtoanTG["sotien"], dataAddthanhtoanTG["noidung"], dataAddthanhtoanTG["khachhangid"], dataAddthanhtoanTG["HDTGid"])
    sql.insert(insert_ttTGFn)
    # print("da insert xong")
    
    res = {}
    return jsonify(res)

##---------------------------HẢI-------------------------------------------------------------
@app.route('/danhba/<id>')
def danhba(id):
    
    sql = SQL_Server()
    query = " select dbo.ThanhVien.HoTen, dbo.NhanVien.Capbac, dbo.NhanVien.ViTri, dbo.ThanhVien.Sdt, dbo.NhanVien.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.NhanVien "
    query += "where dbo.ThanhVien.Id = dbo.NhanVien.ThanVienID AND dbo.NhanVien.Capbac =N'Trưởng phòng'"
    tmp = sql.select(query)
    del sql
    # print(tmp)

    return render_template("Danhba.html" , data = tmp, id = id)


@app.route('/xemchitiet/<id>', methods = ['GET'])
def xemchitiet(id):

    
    sql = SQL_Server()
    query = "select dbo.ThanhVien.HoTen, dbo.ThanhVien.Sdt, dbo.ThanhVien.Nsinh, dbo.NhanVien.ViTri, dbo.NhanVien.Capbac, dbo.ThanhVien.Email from dbo.ThanhVien, dbo.NhanVien "
    query+="where dbo.ThanhVien.Id = dbo.NhanVien.ThanVienID "
    query+=" AND dbo.NhanVien.Id = " +str(id) 
    tmp = sql.select(query)
    del sql
    return render_template("XemChiTiet.html", data = tmp)

@app.route('/deactive', methods = ['POST'])
def deactive():

    sql = SQL_Server()
    data = request.form['hopdong']
    id = data.split(' ')
    data = id[-1]
    tmp = id[0]
    query1 = "UPDATE dbo.ThanhVien SET Activate = " +str(tmp)+" FROM dbo.ThanhVien INNER JOIN dbo.NhanVien ON (dbo.ThanhVien.Id = dbo.NhanVien.ThanVienID) WHERE dbo.NhanVien.Id = "+str(data)
    sql.insert(query1)
    ress = {}
    ress['status'] = "no"
    return jsonify(ress)

@app.route('/updateDB/<id>', methods = ['POST'])
def updateDB(id):

    sql = SQL_Server()
    mien = request.form['mien']
    loai = request.form['loai']
    if loai == "Nhân viên" : 
        loai = 0
    elif loai == "Khách hàng":
        loai = 1
    else:
        loai =2
    query = "select dbo.ThanhVien.HoTen, dbo.NhanVien.Capbac, dbo.NhanVien.ViTri, dbo.ThanhVien.Sdt, dbo.NhanVien.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.NhanVien where dbo.ThanhVien.Tinh = N'{}' and dbo.ThanhVien.Loai= {} and dbo.ThanhVien.Id = dbo.NhanVien.ThanVienID"
    query = query.format(mien,loai)  
    tmp = sql.select(query)
    
    del sql
    return render_template("Danhba.html" , data = tmp , id =  id)


@app.route('/search/<id>', methods = ['POST'])
def search(id):

    sql = SQL_Server()
    search = request.form['search']
    query = "select dbo.ThanhVien.HoTen, dbo.NhanVien.Capbac, dbo.NhanVien.ViTri, dbo.ThanhVien.Sdt, dbo.NhanVien.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.NhanVien where dbo.NhanVien.ThanVienID = dbo.ThanhVien.Id and (dbo.ThanhVien.Username = '{}' "
    query+= " or dbo.ThanhVien.HoTen = N'{}' or dbo.ThanhVien.CMND = '{}'  or dbo.ThanhVien.Sdt = '{}') " 
                
    query = query.format(search,search,search,search)  
    # print(query)
    tmp = sql.select(query)
    # print(tmp)
    del sql
    return render_template("Danhba.html" , data = tmp,id =  id)


# Hoàng Đức Hải, [07.07.20 01:22]
@app.route('/danhbaKH/<id>')
def danhbaKH(id):
    
    sql = SQL_Server()
    query = " select dbo.ThanhVien.HoTen, dbo.KhachHang.Chungthuctaisan, dbo.ThanhVien.CMND, dbo.ThanhVien.Sdt, dbo.KhachHang.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.KhachHang "
    query += "where dbo.ThanhVien.Id = dbo.KhachHang.ThanVienID"
    tmp = sql.select(query)
    del sql
    print(tmp)
    return render_template("DanhbaKH.html" , data = tmp, id = id)


@app.route('/xemchitietKH/<id>', methods = ['GET'])
def xemchitietKH(id):

    sql = SQL_Server()
    query = "select dbo.ThanhVien.HoTen, dbo.ThanhVien.DiaChi, dbo.ThanhVien.Nsinh,dbo.ThanhVien.Sdt, dbo.ThanhVien.Email, dbo.KhachHang.Chukidientu from dbo.ThanhVien, dbo.KhachHang "
    query+="where dbo.ThanhVien.Id = dbo.KhachHang.ThanVienID "
    query+=" AND dbo.KhachHang.Id = " +str(id) 
    tmp = sql.select(query)
    del sql
    print(tmp)
    return render_template("xemchitietKH.html", data = tmp)

# Hoàng Đức Hải, [07.07.20 01:23]
@app.route('/deactiveKH', methods = ['POST'])
def deactiveKH():
    sql = SQL_Server()
    data = request.form['khachhang']
    id = data.split(' ')
    data = id[-1]
    tmp = id[0]
    query1 = "UPDATE dbo.ThanhVien SET Activate = " +str(tmp)+" FROM dbo.ThanhVien INNER JOIN dbo.KhachHang ON (dbo.ThanhVien.Id = dbo.KhachHang.ThanVienID) WHERE dbo.KhachHang.Id = "+str(data)
    print(query1)
    sql.insert(query1)
    ress = {}
    ress['status'] = "no"
    return jsonify(ress)

# Hoàng Đức Hải, [07.07.20 01:23]
@app.route('/updateDBKH/<id>', methods = ['POST'])
def updateDBKH(id):

    sql = SQL_Server()
    mien = request.form['mien']
    query = "select dbo.ThanhVien.HoTen, dbo.KhachHang.Chungthuctaisan, dbo.ThanhVien.CMND, dbo.ThanhVien.Sdt, dbo.KhachHang.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.KhachHang where dbo.ThanhVien.Tinh = N'{}' and dbo.ThanhVien.Loai= '1' and dbo.ThanhVien.Id = dbo.KhachHang.ThanVienID"
    query = query.format(mien)  
    tmp = sql.select(query)
    
    del sql
    return render_template("DanhbaKH.html" , data = tmp)

# Hoàng Đức Hải, [07.07.20 01:23]
@app.route('/searchKH/<id>', methods = ['POST'])
def searchKH(id):

    sql = SQL_Server()
    search = request.form['search']
    query = "select dbo.ThanhVien.HoTen, dbo.KhachHang.Chungthuctaisan, dbo.ThanhVien.CMND, dbo.ThanhVien.Sdt, dbo.KhachHang.Id, dbo.ThanhVien.Activate from dbo.ThanhVien, dbo.KhachHang where dbo.KhachHang.ThanVienID = dbo.ThanhVien.Id and (dbo.ThanhVien.Username = '{}' "
    query+= " or dbo.ThanhVien.HoTen = N'{}' or dbo.ThanhVien.CMND = '{}'  or dbo.ThanhVien.Sdt = '{}') " 
                
    query = query.format(search,search,search,search)  
    print(query)
    tmp = sql.select(query)
    print(tmp)
    del sql
    return render_template("DanhbaKH.html" , data = tmp, id = id)

if __name__ == "__main__":

    app.run(host = '192.168.16.100', debug=True)