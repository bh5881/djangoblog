import pymysql

db_config= {
    'host':'127.0.0.1',
    'port':3306,
    'user': 'root',
    'password':'qwe123',
    'db':'tzproject',
    'charset':'utf8'
}
conn = pymysql.connect(**db_config)
cur = conn.cursor()
sql3 = """INSERT INTO tb_tag(name, create_time, update_time, is_delete) values
('Python基础', now(), now(), 0),
('Python高级', now(), now(), 0),
('Python函数', now(), now(), 0),
('PythonGUI', now(), now(), 0),
('Linux教程', now(), now(), 0),
('Python框架', now(), now(), 0);"""
cur.execute(sql3)
conn.commit()