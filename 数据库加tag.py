import pymysql

db_config= {
    'host':'127.0.0.1',
    'port':3306,
    'user': 'root',
    'password':'qwe123',
    'db':'tzproject',
    'charset':'utf8'
}
# conn = pymysql.connect(**db_config)
# cur = conn.cursor()
# # sql = 'select * from test190506'
# # aa = cur.execute(sql)
# # print(cur.fetchall())
# sql2 = 'insert into test190506 values(8,"成功","D:/OneDrive - f.b.school.nz/360 1605-A01_2019-03-24-20-02-22/BY_3RD_EmailMaster.apk",10333524,"2019-03-24 20:06:53","0fdd9e01613652aa38fc3716b1bd0f82,0fdd9e01613652aa38fc3716b1")'
# cur.execute(sql2)
# sq3 = 'select * from test190506'
# cur.execute(sq3)
# conn.commit()
#
# print(cur.fetchall())
conn = pymysql.connect(**db_config)
cur = conn.cursor()
# sql = 'select * from test190506'
# aa = cur.execute(sql)
# print(cur.fetchall())
# sql2 = 'insert into test190506 values(8,"成功","D:/OneDrive - f.b.school.nz/360 1605-A01_2019-03-24-20-02-22/BY_3RD_EmailMaster.apk",10333524,"2019-03-24 20:06:53","0fdd9e01613652aa38fc3716b1bd0f82,0fdd9e01613652aa38fc3716b1")'
# cur.execute(sql2)
a = 1
b = "ckniukkl"
print(type(a))
# sql4 = 'insert into test190506(id,res) values(1,"333")'
# cur.execute(sql4)
# sql6 = "insert into test190506(id,res) VALUES(%d,'%s')"%(a,b)#此处应该这样写
# cur.execute(sql6)
# sql5 = "delete from test190506"
# cur.execute(sql5)
# sq3 = 'select * from test190506'
sql3 = """INSERT INTO tb_tag(name, create_time, update_time, is_delete) values
('Python基础', now(), now(), 0),
('Python高级', now(), now(), 0),
('Python函数', now(), now(), 0),
('PythonGUI', now(), now(), 0),
('Linux教程', now(), now(), 0),
('Python框架', now(), now(), 0);"""

cur.execute(sql3)
conn.commit()

print(cur.fetchall())