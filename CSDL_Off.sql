CREATE TABLE ThanhVien (
  
	Id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	HoTen nvarchar(255) not null,
	CMND varchar(100) not null,
	DiaChi nvarchar(255) not null,
	Tinh nvarchar(255) not null,
	Username varchar(100) not null,
	Password  varchar(100) not null,
	Nsinh date not null,
	Email varchar(100) not null,
	Sdt varchar(100) not null,
	Loai int not null,
	Activate int not null
);

CREATE TABLE PhongGiaoDich(

	Id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	Ten nvarchar(100),
	DiaChi nvarchar(100),
	Tinh nvarchar(100)

);

CREATE TABLE NhanVien(
	
	Id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	ViTri nvarchar(100),
	Capbac nvarchar(100),
	Diemthuong int,
	NamExp int,
	HesoLuong float,
	FaceId nvarchar(MAX),
	ImgCMND1 nvarchar(MAX),
	ImgCMND2 nvarchar(MAX),
	ThanVienID int FOREIGN KEY REFERENCES ThanhVien(Id),
	
);

CREATE TABLE KhachHang(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	Chukidientu varchar(MAX),
	Chungthuctaisan varchar(255) NOT NULL,
	Diem int,
	ThanVienID int FOREIGN KEY REFERENCES ThanhVien(Id)

);

CREATE TABLE BangLuong(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayBD date,
	NgayTH date,
	Songaydilam int,
	Songaynghi int,
	TongTien float,
	NhanVienID int FOREIGN KEY REFERENCES NhanVien(Id)
);

CREATE TABLE BangChamCong(
	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayLV date,
	TimeDetails nvarchar(255),
	TgianMuon int,
	NhanVienID int FOREIGN KEY REFERENCES NhanVien(Id)
);

CREATE TABLE HopDongTraGop(
	
	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayMoHD date,
	TenSP nvarchar(255),
	Giatri float,
	ThoiHan int,
	Tratruoc float,
	Moithang float,
	Laisuat float,
	NhanVienID int FOREIGN KEY REFERENCES NhanVien(Id),
	KhacHangID int FOREIGN KEY REFERENCES KhachHang(Id),
	PGDId int FOREIGN KEY REFERENCES PhongGiaoDich(Id),
	Activate int
);

CREATE TABLE HopDongMoTheTD(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayMoThe  date,
	Hanmuc float,
	ChuKi int,
	Sothang int,
	HanmucChiTieu float,
	SoThe varchar(100),
	KhacHangID int FOREIGN KEY REFERENCES KhachHang(Id),
	PGDId int FOREIGN KEY REFERENCES PhongGiaoDich(Id),
	Activate int
);

CREATE TABLE ThanhToanHDTG(
	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayTT date,
	Thang int,
	Sotien float,
	Noidung nvarchar(255),
	KhacHangID int FOREIGN KEY REFERENCES KhachHang(Id),
	HDTGId int FOREIGN KEY REFERENCES HopDongTraGop(Id)

);
CREATE TABLE ThongBao(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NoiDung nvarchar(MAX),
	NgayTB date,
	KhacHangID int FOREIGN KEY REFERENCES KhachHang(Id)
);

CREATE TABLE ThanhToanTheTD(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	NgayTT date,
	ThoiHan int,
	Sotien float,
	Noidung nvarchar(255),
	KhacHangID int FOREIGN KEY REFERENCES KhachHang(Id),
	HDTTDID int  FOREIGN KEY REFERENCES HopDongMoTheTD(Id)
);

CREATE TABLE FaceID(

	Id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	ThanVienID int FOREIGN KEY REFERENCES ThanhVien(Id),
	ft1 float,ft2 float,ft3 float,ft4 float,ft5 float,ft6 float,ft7 float,ft8 float,ft9 float,ft10 float,ft11 float,ft12 float,ft13 float,ft14 float,ft15 float,ft16 float,ft17 float,ft18 float,ft19 float,ft20 float,ft21 float,ft22 float,ft23 float,ft24 float,ft25 float,ft26 float,ft27 float,ft28 float,ft29 float,ft30 float,ft31 float,ft32 float,ft33 float,ft34 float,ft35 float,ft36 float,ft37 float,ft38 float,ft39 float,ft40 float,ft41 float,ft42 float,ft43 float,ft44 float,ft45 float,ft46 float,ft47 float,ft48 float,ft49 float,ft50 float,ft51 float,ft52 float,ft53 float,ft54 float,ft55 float,ft56 float,ft57 float,ft58 float,ft59 float,ft60 float,ft61 float,ft62 float,ft63 float,ft64 float,ft65 float,ft66 float,ft67 float,ft68 float,ft69 float,ft70 
	float,ft71 float,ft72 float,ft73 float,ft74 float,ft75 float,ft76 float,ft77 float,ft78 float,ft79 float,ft80 float,ft81 float,ft82 float,ft83 float,ft84 float,ft85 float,ft86 float,ft87 float,ft88 float,ft89 float,ft90 float,ft91 float,ft92 float,ft93 float,ft94 float,ft95 float,ft96 float,ft97 float,ft98 float,ft99 float,ft100 float,ft101 float,ft102 float,ft103 float,ft104 float,ft105 float,ft106 float,ft107 float,ft108 float,ft109 float,ft110 float,ft111 float,ft112 float,ft113 float,ft114 float,ft115 float,ft116 float,ft117 float,ft118 float,ft119 float,ft120 float,ft121 float,ft122 float,ft123 float,ft124 float,ft125 float,ft126 float,ft127 float,ft128 float,ft129 float,ft130 float,ft131 float,ft132 float,ft133 float,ft134 float,ft135 float,ft136 float,ft137 float,ft138 float,ft139 float,ft140 float,ft141 float,ft142 float,ft143 float,ft144 float,ft145 float,ft146 float,ft147 float,ft148 float,ft149 float,ft150 float,ft151 float,ft152 float,ft153 float,ft154 float,ft155 float,ft156 float,ft157 float,ft158 float,ft159 float,ft160 float,ft161 float,ft162 float,ft163 float,ft164 float,ft165 float,ft166 float,ft167 float,ft168 float,ft169 float,ft170 float,ft171 float,ft172 float,ft173 float,ft174 float,ft175 float,ft176 float,ft177 float,ft178 float,ft179 float,ft180 float,ft181 float,ft182 float,ft183 float,ft184 float,ft185 float,ft186 float,ft187 float,ft188 float,ft189 float,ft190 float,ft191 float,ft192 float,ft193 float,ft194 float,ft195 float,ft196 float,ft197 float,ft198 float,ft199 float,ft200 float,ft201 float,ft202 float,ft203 float,ft204 float,ft205 float,ft206 float,ft207 float,ft208 float,ft209 float,ft210 float,ft211 float,ft212 float,ft213 float,ft214 float,ft215 float,ft216 float,ft217 float,ft218 float,ft219 float,ft220 float,ft221 float,ft222 float,ft223 float,ft224 float,ft225 float,ft226 float,ft227 float,ft228 float,ft229 float,ft230 float,ft231 float,ft232 float,ft233 float,ft234 float,ft235 float,ft236 
	float,ft237 float,ft238 float,ft239 float,ft240 float,ft241 float,ft242 float,ft243 float,ft244 float,ft245 float,ft246 float,ft247 float,ft248 float,ft249 float,ft250 float,ft251 float,ft252 float,ft253 float,ft254 float,ft255 float,ft256 float,ft257 float,ft258 float,ft259 float,ft260 float,ft261 float,ft262 float,ft263 float,ft264 float,ft265 float,ft266 float,ft267 float,ft268 float,ft269 float,ft270 float,ft271 float,ft272 float,ft273 float,ft274 float,ft275 float,ft276 float,ft277 float,ft278 float,ft279 float,ft280 float,ft281 float,ft282 float,ft283 float,ft284 float,ft285 float,ft286 float,ft287 float,ft288 float,ft289 float,ft290 float,ft291 float,ft292 float,ft293 float,ft294 float,ft295 float,ft296 float,ft297 float,ft298 float,ft299 float,ft300 float,ft301 float,ft302 float,ft303 float,ft304 float,ft305 float,ft306 float,ft307 float,ft308 float,ft309 float,ft310 float,ft311 float,ft312 float,ft313 float,ft314 float,ft315 float,ft316 float,ft317 float,ft318 float,ft319 float,ft320 float,ft321 float,ft322 float,ft323 float,ft324 float,ft325 float,ft326 float,ft327 float,ft328 float,ft329 float,ft330 float,ft331 float,ft332 float,ft333 float,ft334 float,ft335 float,ft336 float,ft337 float,ft338 float,ft339 float,ft340 float,ft341 float,ft342 float,ft343 float,ft344 float,ft345 float,ft346 float,ft347 float,ft348 float,ft349 float,ft350 float,ft351 float,ft352 float,ft353 float,ft354 float,ft355 float,ft356 float,ft357 float,ft358 float,ft359 float,ft360 float,ft361 float,ft362 float,ft363 float,ft364 float,ft365 float,ft366 float,ft367 float,ft368 float,ft369 float,ft370 float,ft371 float,ft372 float,ft373 float,ft374 float,ft375 float,ft376 float,ft377 float,ft378 float,ft379 float,ft380 float,ft381 float,ft382 float,ft383 float,ft384 float,ft385 float,ft386 float,ft387 
	float,ft388 float,ft389 float,ft390 float,ft391 float,ft392 float,ft393 float,ft394 float,ft395 float,ft396 float,ft397 float,ft398 float,ft399 float,ft400 float,ft401 float,ft402 float,ft403 float,ft404 float,ft405 float,ft406 float,ft407 float,ft408 float,ft409 float,ft410 float,ft411 float,ft412 float,ft413 float,ft414 float,ft415 float,ft416 float,ft417 float,ft418 float,ft419 float,ft420 float,ft421 float,ft422 float,ft423 float,ft424 float,ft425 float,ft426 float,ft427 float,ft428 float,ft429 float,ft430 float,ft431 float,ft432 float,ft433 float,ft434 float,ft435 float,ft436 float,ft437 float,ft438 float,ft439 float,ft440 float,ft441 float,ft442 float,ft443 float,ft444 float,ft445 float,ft446 float,ft447 float,ft448 float,ft449 float,ft450 float,ft451 float,ft452 float,ft453 float,ft454 float,ft455 float,ft456 float,ft457 float,ft458 float,ft459 float,ft460 float,ft461 float,ft462 float,ft463 float,ft464 float,ft465 float,ft466 float,ft467 float,ft468 float,ft469 float,ft470 float,ft471 float,ft472 float,ft473 float,ft474 float,ft475 float,ft476 float,ft477 float,ft478 float,ft479 float,ft480 float,ft481 float,ft482 float,ft483 float,ft484 float,ft485 float,ft486 float,ft487 float,ft488 float,ft489 float,ft490 float,ft491 float,ft492 float,ft493 float,ft494 float,ft495 float,ft496 float,ft497 float,ft498 float,ft499 float,ft500 float,ft501 float,ft502 float,ft503 float,ft504 float,ft505 float,ft506 float,ft507 float,ft508 float,ft509 float,ft510 float,ft511 float,ft512 float
);